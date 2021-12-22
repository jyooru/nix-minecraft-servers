import json
from logging import getLogger
from typing import Dict, Union

from .common import get_latest_major_versions
from .paper import Project


log = getLogger(__name__)


def generate() -> Dict[str, Dict[str, Union[str, int]]]:
    project = Project.get("velocity")
    major_versions_str = get_latest_major_versions(
        [version for version in project.versions if not version.endswith("SNAPSHOT")]
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
    with open("pkgs/velocity.json", "w") as file:
        data = generate()
        log.info(f"[b]Found {len(data.keys())} versions for Velocity")
        json.dump(data, file, indent=2)
        file.write("\n")


if __name__ == "__main__":
    main()
