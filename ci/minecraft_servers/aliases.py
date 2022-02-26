from typing import Dict, List

from semantic_version import NpmSpec, Version

from .common import Aliases, Sources


def replace(string: str) -> str:
    return (
        string.replace("~", "")
        .replace(" Pre-Release ", "-pre")
        .replace(".", "_")
        .replace("-", "_")
        .replace(" ", "_")
    )


def clean(package: str, aliases: Dict[str, Version]) -> Dict[str, str]:
    result = {}
    for key, value in aliases.items():
        # if this alias is for the latest version then alias should just be package
        alias = package if key == "" else f"{package}_{replace(key)}"
        result[alias] = f"{package}_{replace(str(value))}"
    return result


def generate(package: str, sources: Sources) -> Aliases:
    # releases that don't follow a versioning scheme and should not be aliased
    ignore = [
        "1.RV-Pre1",
        "3D Shareware v1.34",
    ]

    versions = [
        Version.coerce(source["version"])
        for source in sources
        if "." in str(source["version"])  # filter out snapshots
        if source["version"] not in ignore
    ]

    for version in versions:
        if NpmSpec(f"~{version.major}.{version.minor}") is None:
            raise Exception(version)

    latest_spec = NpmSpec("")
    major_specs = {NpmSpec(f"~{version.major}") for version in versions}
    minor_specs = {NpmSpec(f"~{version.major}.{version.minor}") for version in versions}
    specs = {latest_spec} | major_specs | minor_specs

    aliases = {spec.expression: spec.select(versions) for spec in specs}

    return clean(package, aliases)


def dump(aliases: List[Aliases]) -> Aliases:
    left: Aliases = {}
    for right in aliases:
        left = left | right
    return left
