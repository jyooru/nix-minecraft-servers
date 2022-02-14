from logging import getLogger
from typing import Dict, Union

from .common import get_latest_major_versions
from .paper import Project


log = getLogger(__name__)


def generate() -> Dict[str, Dict[str, Union[str, int]]]:
    project = Project.get("waterfall")
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
