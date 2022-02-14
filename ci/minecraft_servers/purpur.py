from asyncio import gather
from dataclasses import dataclass
from logging import getLogger
from typing import Dict, List, Union

from aiohttp import ClientSession
from dataclasses_json import DataClassJsonMixin

from .common import get_sha256


log = getLogger(__name__)


@dataclass
class Build(DataClassJsonMixin):
    build: int
    commits: List[Dict[str, Union[str, int]]]
    duration: int
    md5: str
    project: str
    result: str
    timestamp: int
    version: str

    def get_url(self) -> str:
        return f"https://api.purpurmc.org/v2/{self.project}/{self.version}/{self.build}/download"  # noqa: E501

    def output_for_nix(self) -> Dict[str, Union[str, int]]:
        url = self.get_url()
        return {
            "url": url,
            "sha256": get_sha256(url),
            "version": self.version,
            "build": int(self.build),
        }


@dataclass
class VersionBuilds(DataClassJsonMixin):
    all: List[str]
    latest: str


@dataclass
class Version(DataClassJsonMixin):
    builds: VersionBuilds
    project: str
    version: str

    async def get_build(self, session: ClientSession, build: str) -> Build:
        async with session.get(
            f"/v2/{self.project}/{self.version}/{build}"
        ) as response:
            return Build.from_dict(await response.json())


@dataclass
class Project(DataClassJsonMixin):
    project: str
    versions: List[str]

    @staticmethod
    async def get(session: ClientSession, project: str) -> "Project":
        async with session.get(f"/v2/{project}") as response:
            return Project.from_dict(await response.json())

    async def get_version(self, session: ClientSession, version: str) -> Version:
        async with session.get(f"/v2/{self.project}/{version}") as response:
            return Version.from_dict(await response.json())


async def generate() -> Dict[str, Dict[str, Union[str, int]]]:
    async with ClientSession("https://api.purpurmc.org") as session:
        project = await Project.get(session, "purpur")
        versions = await gather(
            *[project.get_version(session, version) for version in project.versions]
        )
        builds = await gather(
            *[version.get_build(session, version.builds.latest) for version in versions]
        )

    return {build.version: build.output_for_nix() for build in builds}
