from asyncio import gather

from aiohttp import ClientSession

from .common import Sources, trace_configs
from .paper import Project


async def generate() -> Sources:
    async with ClientSession(
        "https://papermc.io",
        trace_configs=trace_configs,
    ) as session:
        project = await Project.get(session, "velocity")
        versions = await gather(
            *[
                project.get_version(session, version)
                for version in project.versions
                if not version.endswith("SNAPSHOT")
            ]
        )
        builds = await gather(
            *[version.get_build(session, max(version.builds)) for version in versions]
        )

    return [build.output_for_nix() for build in builds]
