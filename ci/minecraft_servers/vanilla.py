from asyncio import gather
from dataclasses import dataclass, field
from datetime import datetime
from logging import getLogger
from typing import Any, Dict, List, Optional, Tuple

from aiohttp import ClientSession
from dataclasses_json import DataClassJsonMixin, LetterCase, config
from marshmallow import fields

from .common import trace_configs


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

        try:
            self._manifest
        except AttributeError:
            async with session.get(self.url) as response:
                self._manifest = await response.json()
        return self._manifest

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

    async def get_server(
        self, session: ClientSession
    ) -> Tuple[str, Optional[Download]]:
        """
        Return this version's ID along with the Download object for this version's
        server. If the version does not have a server download avilable, None is
        returned instead of a Download object.
        """
        downloads = await self.get_downloads(session)
        return (self.id, downloads.get("server"))


async def get_versions(session: ClientSession) -> Dict[str, Version]:
    """Return a dictionary of Version objects for all available versions."""
    async with session.get(
        "https://launchermeta.mojang.com/mc/game/version_manifest.json"
    ) as response:
        json = await response.json()
        versions = [Version.from_dict(version) for version in json["versions"]]
        return {version.id: version for version in versions}


async def generate() -> List[Dict[str, Any]]:
    """
    Return a dictionary containing the latest url, sha1 and version for each major
    release.
    """
    async with ClientSession(trace_configs=trace_configs) as session:
        versions = await get_versions(session)
        servers = await gather(
            *[version.get_server(session) for version in versions.values()]
        )
        sources = {
            server[0]: server[1].to_dict()
            for server in servers
            if server[1] is not None  # versions < 1.2 do not have a server
        }

        for key, value in sources.items():
            del value["size"]
            value["version"] = versions[key].id
            value["javaVersion"] = await versions[key].get_java_version(session)

    return list(sources.values())
