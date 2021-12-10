from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict

import requests
from dataclasses_json import DataClassJsonMixin, LetterCase, config
from marshmallow import fields


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
            letter_case=LetterCase.CAMEL,
        )
    )

    def get_manifest(self) -> Any:
        response = requests.get(self.url)
        response.raise_for_status()
        return response.json()

    def get_downloads(self) -> Dict[str, Download]:
        manifest = self.get_manifest()
        return {
            key: Download.from_dict(value)
            for key, value in manifest["downloads"].items()
        }

    def get_server(self) -> Download:
        return self.get_downloads()["server"]


def get_versions() -> Dict[str, Version]:
    response = requests.get(
        "https://launchermeta.mojang.com/mc/game/version_manifest.json"
    )
    response.raise_for_status()
    data = response.json()
    versions_list = [Version.from_dict(version) for version in data["versions"]]
    versions_dict = {version.id: version for version in versions_list}
    return versions_dict
