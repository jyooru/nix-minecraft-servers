from asyncio import gather
from logging import getLogger
from typing import Dict, Union

from aiohttp import ClientSession

from .common import get_latest_major_versions, get_major_release
from .paper import Project

log = getLogger(__name__)


async def generate() -> Dict[str, Dict[str, Union[str, int]]]:
    async with ClientSession("https://papermc.io") as session:
        project = await Project.get(session, "waterfall")
        major_versions = get_latest_major_versions(project.versions).values()
        versions = await gather(
            *[project.get_version(session, version) for version in major_versions]
        )
        builds = await gather(
            *[version.get_build(session, max(version.builds)) for version in versions]
        )

    return {
        get_major_release(build.version): build.output_for_nix() for build in builds
    }
