import json
from dataclasses import dataclass
from logging import getLogger
from typing import Dict, List, Union

from dataclasses_json import DataClassJsonMixin

from .common import get_json, get_latest_major_versions, get_sha256


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
        return {
            "url": self.get_url(),
            "sha256": get_sha256(self.get_url()),
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

    def get_build(self, build: str) -> Build:
        return Build.from_dict(
            get_json(
                f"https://api.purpurmc.org/v2/{self.project}/{self.version}/{build}"
            )
        )


@dataclass
class Project(DataClassJsonMixin):
    project: str
    versions: List[str]

    @staticmethod
    def get(project: str) -> "Project":
        return Project.from_dict(get_json(f"https://api.purpurmc.org/v2/{project}"))

    def get_version(self, version: str) -> Version:
        return Version.from_dict(
            get_json(f"https://api.purpurmc.org/v2/{self.project}/{version}")
        )


def generate() -> Dict[str, Dict[str, Union[str, int]]]:
    project = Project.get("purpur")
    major_versions_str = get_latest_major_versions(project.versions)
    major_versions_Version = {
        major_version: project.get_version(version)
        for major_version, version in major_versions_str.items()
    }
    major_versions_Build = {
        major_version: version.get_build(version.builds.latest)
        for major_version, version in major_versions_Version.items()
    }
    major_versions_dict = {
        major_version: build.output_for_nix()
        for major_version, build in major_versions_Build.items()
    }
    return major_versions_dict


def main() -> None:
    with open("packages/purpur/sources.json", "w") as file:
        data = generate()
        log.info(f"[b]Found {len(data.keys())} versions for Purpur")
        json.dump(data, file, indent=2)
        file.write("\n")


if __name__ == "__main__":
    main()
