import json
from dataclasses import dataclass
from typing import Dict, List, Union

import requests
from dataclasses_json import DataClassJsonMixin

from .common import get_latest_major_versions


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

    def output_for_nix(self) -> Dict[str, Union[str, int]]:
        return {
            "url": f"https://papermc.io/api/v2/projects/{self.project_id}/versions/{self.version}/builds/{self.build}/downloads/application",
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

    def get_build(self, build: int) -> Build:
        response = requests.get(
            f"https://papermc.io/api/v2/projects/{self.project_id}/versions/{self.version}/builds/{build}"
        )
        response.raise_for_status()
        return Build.from_dict(response.json())


@dataclass
class Project(DataClassJsonMixin):
    project_id: str
    project_name: str
    version_groups: List[str]
    versions: List[str]

    def get(project_id: str) -> "Project":
        response = requests.get(f"https://papermc.io/api/v2/projects/{project_id}")
        response.raise_for_status()
        return Project.from_dict(response.json())

    def get_version(self, version: str) -> Version:
        response = requests.get(
            f"https://papermc.io/api/v2/projects/{self.project_id}/versions/{version}"
        )
        response.raise_for_status()
        return Version.from_dict(response.json())


def generate() -> Dict[str, Dict[str, str]]:
    project = Project.get("paper")
    major_versions_str = get_latest_major_versions(project.versions)
    major_versions_Version = {
        major_version: project.get_version(version)
        for major_version, version in major_versions_str.items()
    }
    major_versions_Build = {
        major_version: version.get_build(max(version.builds))
        for major_version, version in major_versions_Version.items()
    }
    major_versions_dict = {
        major_version: build.output_for_nix()
        for major_version, build in major_versions_Build.items()
    }
    return major_versions_dict


def main() -> None:
    with open("pkgs/paper.json", "w") as file:
        json.dump(generate(), file, indent=2)
        file.write("\n")


if __name__ == "__main__":
    main()
