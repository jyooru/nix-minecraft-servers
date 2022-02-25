from typing import List, Union

from semantic_version import NpmSpec, Version

from .common import Aliases, Sources


def generate(package: str, sources: Sources) -> Aliases:
    versions = [Version.coerce(source["version"]) for source in sources]

    major_specs = {NpmSpec(f"~{version.major}") for version in versions}
    minor_specs = {NpmSpec(f"~{version.major}.{version.minor}") for version in versions}
    specs = major_specs | minor_specs

    aliases = {spec.expression: spec.select(versions) for spec in specs}

    def clean(version: Union[str, Version]) -> str:
        if isinstance(version, Version):
            version = str(version)
        return package + "_" + version.replace("~", "").replace(".", "_")

    return {clean(key): clean(value) for key, value in aliases.items()}


def dump(aliases: List[Aliases]) -> Aliases:
    left: Aliases = {}
    for right in aliases:
        left = left | right
    return left
