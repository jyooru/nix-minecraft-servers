from hashlib import sha256
from logging import getLogger
from typing import Any, Dict, List

from rich.console import Console
from rich.text import Text
import requests


console = Console()
log = getLogger(__name__)


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


def get(url: str, should_log: bool = True) -> requests.Response:
    response = requests.get(url)
    response.raise_for_status()
    if should_log:
        log.debug(f"GET {url} {response.status_code}")
    return response


def get_json(*args, **kwargs) -> Any:
    return get(*args, **kwargs).json()


def get_sha256(url: str) -> str:
    with console.status(
        Text.from_markup(f"Manually hashing file [u bright_blue]{url}")
    ):
        response = get(url, should_log=False)
        hash = sha256(response.content).hexdigest()
    log.debug(f"GET {url} {response.status_code} [bold magenta]{hash}")
    return hash
