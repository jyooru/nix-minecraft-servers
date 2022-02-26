from logging import getLogger
from types import SimpleNamespace
from typing import Dict, List, Union

import aiohttp
from aiohttp import ClientSession, TraceRequestEndParams, TraceRequestStartParams
from rich.console import Console


console = Console()
log = getLogger(__name__)


Aliases = Dict[str, str]
Source = Dict[str, Union[int, str]]
Sources = List[Source]


def get_major_release(version: str) -> str:
    """
    Return the major release for a version. The major release for 1.17 and
    1.17.1 is 1.17.
    """
    if not len(version.split(".")) >= 2:
        raise ValueError(f"version not in expected format: '{version}'")
    return ".".join(version.split(".")[:2])


def group_major_versions(versions: List[str]) -> Dict[str, List[str]]:
    """
    Return a dictionary containing each version grouped by each major version.
    The key "1.17" contains a list with two strings, one for "1.17" and another
    for "1.17.1".
    """
    groups: Dict[str, List[str]] = {}
    for version in versions:
        major_version = get_major_release(version)
        if major_version not in groups:
            groups[major_version] = []
        groups[major_version].append(version)
    return groups


def get_latest_major_versions(versions: List[str]) -> Dict[str, str]:
    """
    Return a dictionary containing the latest version for each major version.
    The latest major version for 1.16 is 1.16.5, so the key "1.16" contains
    the string "1.16.5".
    """
    return {
        major_release: sorted(releases, reverse=True)[0]
        for major_release, releases in group_major_versions(versions).items()
    }


async def on_request_start(
    session: ClientSession,
    context: SimpleNamespace,
    params: TraceRequestStartParams,
) -> None:
    log.debug(f"-> {params.method} {params.url}")


async def on_request_end(
    session: ClientSession,
    context: SimpleNamespace,
    params: TraceRequestEndParams,
) -> None:
    log.debug(f"<- {params.method} {params.url} {params.response.status}")


trace_config = aiohttp.TraceConfig()
trace_config.on_request_start.append(on_request_start)
trace_config.on_request_end.append(on_request_end)
trace_configs = [trace_config]
