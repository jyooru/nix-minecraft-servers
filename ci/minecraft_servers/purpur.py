import json
from asyncio import gather
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Dict, List, Union

import requests
from aiohttp import ClientSession
from dataclasses_json import DataClassJsonMixin
from platformdirs import user_cache_path

from .common import Sources, trace_configs


# until papyrus v2
# https://github.com/PurpurMC/papyrus/issues/1
class Sha256Cache:
    data: Dict[str, str]

    def __init__(self, path: Union[Path, str]) -> None:
        if isinstance(path, str):
            self.path = Path(path)
        else:
            self.path = path

        if self.path.exists():
            with open(str(path)) as file:
                self.data = json.load(file)
        else:
            self.data = {}

    def get(self, url: str) -> str:
        if url not in self.data:
            response = requests.get(url)
            response.raise_for_status()
            self.data[url] = sha256(response.content).hexdigest()

        return self.data[url]

    def save(self) -> None:
        if not self.path.parent.exists():
            self.path.parent.mkdir(parents=True)

        with open(self.path, "w") as file:
            json.dump(self.data, file, indent=2, sort_keys=True)


cache = Sha256Cache(user_cache_path("minecraft-servers") / "purpur.json")


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
            "sha256": cache.get(url),
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


async def generate() -> Sources:
    async with ClientSession(
        "https://api.purpurmc.org",
        trace_configs=trace_configs,
    ) as session:
        project = await Project.get(session, "purpur")
        versions = await gather(
            *[project.get_version(session, version) for version in project.versions]
        )
        builds = await gather(
            *[version.get_build(session, version.builds.latest) for version in versions]
        )

    sources = [build.output_for_nix() for build in builds]
    cache.save()
    return sources
