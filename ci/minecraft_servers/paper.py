import json
from dataclasses import dataclass
from logging import getLogger
from typing import Dict, List, Union

from dataclasses_json import DataClassJsonMixin

from .common import get_json, get_latest_major_versions


log = getLogger(__name__)


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

    def get_build(self, build: int) -> Build:
        return Build.from_dict(
            get_json(
                f"https://papermc.io/api/v2/projects/{self.project_id}/versions/{self.version}/builds/{build}"  # noqa: E501
            )
        )


@dataclass
class Project(DataClassJsonMixin):
    project_id: str
    project_name: str
    version_groups: List[str]
    versions: List[str]

    @staticmethod
    def get(project_id: str) -> "Project":
        return Project.from_dict(
            get_json(f"https://papermc.io/api/v2/projects/{project_id}")
        )

    def get_version(self, version: str) -> Version:
        return Version.from_dict(
            get_json(
                f"https://papermc.io/api/v2/projects/{self.project_id}/versions/{version}"  # noqa: E501
            )
        )


def generate() -> Dict[str, Dict[str, Union[str, int]]]:
    project = Project.get("paper")
    major_versions_str = get_latest_major_versions(
        [
            version
            for version in project.versions
            if not any(["pre" in v for v in version.split("-")])
        ]
    )
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
    with open("packages/paper/sources.json", "w") as file:
        data = generate()
        log.info(f"[b]Found {len(data.keys())} versions for Paper")
        json.dump(data, file, indent=2, sort_keys=True)
        file.write("\n")


if __name__ == "__main__":
    main()
