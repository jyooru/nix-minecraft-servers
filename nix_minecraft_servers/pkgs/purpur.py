import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

import requests
from dataclasses_json import DataClassJsonMixin, LetterCase, config
from marshmallow import fields

@dataclass
class Build(DataClassJsonMixin):
    build: int
    commits: List[Dict[str, Union[str, int]]]
    duration: int
    md5: str
    project: str
    result: str
    timestamp: int
    version: str


@dataclass
class VersionBuilds(DataClassJsonMixin):
    all: List[str]
    latest: str


@dataclass
class Version(DataClassJsonMixin):
    builds: VersionBuilds
    project: str
    version: str

    def get_build(self, build: int) -> Build:
        response = requests.get(
            f"https://api.purpurmc.org/v2/{self.project}/{self.version}/{build}"
        )
        response.raise_for_status()
        return Build.from_dict(response.json())


@dataclass
class Project(DataClassJsonMixin):
    project: str
    versions: List[str]

    def get(project: str) -> "Project":
        response = requests.get(f"https://api.purpurmc.org/v2/{project}")
        response.raise_for_status()
        return Project.from_dict(response.json())

    def get_version(self, version: str) -> Version:
        response = requests.get(f"https://api.purpurmc.org/v2/{self.project}/{version}")
        response.raise_for_status()
        return Version.from_dict(response.json())
