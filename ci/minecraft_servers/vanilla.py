from dataclasses import dataclass, field
from datetime import datetime
from logging import getLogger
from typing import Any, Dict, List, Optional

from aiohttp import ClientSession
from dataclasses_json import DataClassJsonMixin, LetterCase, config
from marshmallow import fields


log = getLogger(__name__)


@dataclass
class Download(DataClassJsonMixin):
    sha1: str
    size: int
    url: str


@dataclass
class Version(DataClassJsonMixin):
    id: str
    type: str
    url: str
    time: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format="iso"),
        )
    )
    release_time: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format="iso"),
            letter_case=LetterCase.CAMEL,  # type: ignore
        )
    )

    async def get_manifest(self, session: ClientSession) -> Any:
        """Return the version's manifest."""
        async with session.get(self.url) as response:
            return await response.json()

    async def get_downloads(self, session: ClientSession) -> Dict[str, Download]:
        """
        Return all downloadable files from the version's manifest, in Download
        objects.
        """
        downloads = (await self.get_manifest(session))["downloads"]
        return {key: Download.from_dict(value) for key, value in downloads.items()}

    async def get_java_version(self, session: ClientSession) -> Any:
        """
        Return the java version specified in a version's manifest, if it is
        present. Versions <= 1.6 do not specify this.
        """
        manifest = await self.get_manifest(session)
        return manifest.get("javaVersion", {}).get("majorVersion", None)

    async def get_server(self, session: ClientSession) -> Optional[Download]:
        """
        If the version has a server download available, return the Download
        object for the server download. If the version does not have a server
        download avilable, return None.
        """
        downloads = await self.get_downloads(session)
        return downloads.get("server")


async def get_versions(session: ClientSession) -> List[Version]:
    """Return a list of Version objects for all available versions."""
    async with session.get(
        "https://launchermeta.mojang.com/mc/game/version_manifest.json"
    ) as response:
        json = await response.json()
        return [Version.from_dict(version) for version in json["versions"]]


def get_major_release(version_id: str) -> str:
    """
    Return the major release for a version. The major release for 1.17 and
    1.17.1 is 1.17.
    """
    if not len(version_id.split(".")) >= 2:
        raise ValueError(f"version not in expected format: '{version_id}'")
    return ".".join(version_id.split(".")[:2])


def group_major_releases(releases: List[Version]) -> Dict[str, List[Version]]:
    """
    Return a dictionary containing each version grouped by each major release.
    The key "1.17" contains a list with two Version objects, one for "1.17"
    and another for "1.17.1".
    """
    groups: Dict[str, List[Version]] = {}
    for release in releases:
        major_release = get_major_release(release.id)
        if major_release not in groups:
            groups[major_release] = []
        groups[major_release].append(release)
    return groups


def get_latest_major_releases(releases: List[Version]) -> Dict[str, Version]:
    """
    Return a dictionary containing the latest version for each major release.
    The latest major release for 1.16 is 1.16.5, so the key "1.16" contains a
    Version object for 1.16.5.
    """
    return {
        major_release: sorted(releases, key=lambda x: x.id, reverse=True)[0]
        for major_release, releases in group_major_releases(releases).items()
    }


async def generate() -> Dict[str, Dict[str, str]]:
    """
    Return a dictionary containing the latest url, sha1 and version for each major
    release.
    """
    async with ClientSession() as session:
        versions = await get_versions(session)
        releases = filter(lambda version: version.type == "release", versions)
        major_releases = get_latest_major_releases(list(releases))
        servers = {
            key: await value.get_server(session)
            for key, value in major_releases.items()
        }

        data = {
            key: Download.schema().dump(value)
            for key, value in servers.items()
            if value is not None  # versions < 1.2 do not have a server
        }
        for key, value in data.items():
            del value["size"]
            value["version"] = major_releases[key].id
            value["javaVersion"] = await major_releases[key].get_java_version(session)
    return data
