from asyncio import gather
from dataclasses import dataclass
from typing import Dict, List

from aiohttp import ClientSession
from dataclasses_json import DataClassJsonMixin

from .common import Source, Sources, trace_configs


@dataclass
class Download(DataClassJsonMixin):
    name: str
    sha256: str


@dataclass
class Build(DataClassJsonMixin):
    build: int
    changes: List[Dict[str, str]]
    channel: str
    downloads: Dict[str, Download]
    project_id: str
    project_name: str
    promoted: bool
    time: str
    version: str

    def output_for_nix(self) -> Source:
        return {
            "url": f"https://papermc.io/api/v2/projects/{self.project_id}/versions/{self.version}/builds/{self.build}/downloads/{self.downloads['application'].name}",  # noqa: E501
            "sha256": self.downloads["application"].sha256,
            "build": self.build,
            "version": self.version,
        }


@dataclass
class Version(DataClassJsonMixin):
    builds: List[int]
    project_id: str
    project_name: str
    version: str

    async def get_build(self, session: ClientSession, build: int) -> Build:
        async with session.get(
            f"/api/v2/projects/{self.project_id}/versions/{self.version}/builds/{build}"
        ) as response:
            return Build.from_dict(await response.json())


@dataclass
class Project(DataClassJsonMixin):
    project_id: str
    project_name: str
    version_groups: List[str]
    versions: List[str]

    @staticmethod
    async def get(session: ClientSession, project_id: str) -> "Project":
        async with session.get(f"/api/v2/projects/{project_id}") as response:
            return Project.from_dict(await response.json())

    async def get_version(self, session: ClientSession, version: str) -> Version:
        async with session.get(
            f"/api/v2/projects/{self.project_id}/versions/{version}"
        ) as response:
            return Version.from_dict(await response.json())


async def generate() -> Sources:
    async with ClientSession(
        "https://papermc.io",
        trace_configs=trace_configs,
    ) as session:
        project = await Project.get(session, "paper")
        versions = await gather(
            *[
                project.get_version(session, version)
                for version in project.versions
                if not any(["pre" in v for v in version.split("-")])
            ]
        )
        builds = await gather(
            *[
                version.get_build(session, max(version.builds))
                for version in versions
                if len(version.builds) > 0
            ]
        )

    return [build.output_for_nix() for build in builds]
