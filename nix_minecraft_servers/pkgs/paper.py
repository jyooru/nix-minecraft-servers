import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

import requests
from dataclasses_json import DataClassJsonMixin, LetterCase, config
from marshmallow import fields



@dataclass
class Download(DataClassJsonMixin):
    name: str
    sha256: str

@dataclass
class Build(DataClassJsonMixin):
    build: int
    changes: List[Dict[str, str]]
    channel: str
    downloads: Dict[str, Download]
    project_id: str
    project_name: str
    promoted: bool
    time:str
    version: str


@dataclass
class Version(DataClassJsonMixin):
    builds: List[int]
    project_id: str
    project_name: str
    version: str

    def get_build(self, build: int) -> Build:
        response = requests.get(
            f"https://papermc.io/api/v2/projects/{self.project_id}/versions/{self.version}/builds/{build}"
        )
        response.raise_for_status()
        return Build.from_dict(response.json())


@dataclass
class Project(DataClassJsonMixin):
    project_id: str
    project_name: str
    version_groups: List[str]
    versions: List[str]

    def get(project_id: str) -> "Project":
        response = requests.get(f"https://papermc.io/api/v2/projects/{project_id}")
        response.raise_for_status()
        return Project.from_dict(response.json())

    def get_version(self, version: str) -> Version:
        response = requests.get(
            f"https://papermc.io/api/v2/projects/{self.project_id}/versions/{version}"
        )
        response.raise_for_status()
        return Version.from_dict(response.json())
