import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

import requests
from dataclasses_json import DataClassJsonMixin, LetterCase, config
from marshmallow import fields
from nix_minecraft_servers.pkgs.common import (
    get_latest_major_versions,
    get_sha256,
    group_major_versions,
)


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
        return f"https://api.purpurmc.org/v2/{self.project}/{self.version}/{self.build}/download"

    def output_for_nix(self) -> Dict[str, Union[str, int]]:
        return {
            "url": self.get_url(),
            "sha256": get_sha256(self.get_url()),
            "version": self.version,
            "build": self.build,
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
        response = requests.get(
            f"https://api.purpurmc.org/v2/{self.project}/{self.version}/{build}"
        )
        response.raise_for_status()
        return Build.from_dict(response.json())


@dataclass
class Project(DataClassJsonMixin):
    project: str
    versions: List[str]

    def get(project: str) -> "Project":
        response = requests.get(f"https://api.purpurmc.org/v2/{project}")
        response.raise_for_status()
        return Project.from_dict(response.json())

    def get_version(self, version: str) -> Version:
        response = requests.get(f"https://api.purpurmc.org/v2/{self.project}/{version}")
        response.raise_for_status()
        return Version.from_dict(response.json())


def generate() -> Dict[str, Dict[str, str]]:
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


def main():
    with open("pkgs/purpur.json", "w") as file:
        json.dump(generate(), file, indent=2)
        file.write("\n")


if __name__ == "__main__":
    main()