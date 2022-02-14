import argparse
import json
from asyncio import gather, run
from logging import getLogger
from typing import Any, List

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

from . import packages, readme


console = Console()
log = getLogger(__name__)


def parse_args(args: List[str] = []) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="minecraft-servers",
        description="Automatically updated Minecraft servers",
    )
    parser.add_argument(
        "-r",
        "--readme",
        action="store_true",
        help="enable readme update on completion",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="path to save output json, defaults to 'packages/{}/sources.json'",
        default="packages/{}/sources.json",
    )
    parser.add_argument(
        "-p",
        "--packages",
        type=str,
        help="packages to fetch, comma seperated",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="increase output verbosity",
    )
    if len(args) == 0:
        return parser.parse_args()
    else:
        return parser.parse_args(args)


async def fetch_package(package: str, output: str) -> None:
    data = await packages[package].generate()
    with open(output.format(package), "w") as file:
        json.dump(data, file, indent=2, sort_keys=True)
        file.write("\n")


async def async_main(args: List[str] = []) -> None:
    parsed_args = parse_args(args)

    if parsed_args.verbose:
        getLogger().setLevel("DEBUG")
    if parsed_args.packages is None:
        parsed_args.packages = set(packages.keys())
    elif parsed_args.packages == "":
        parsed_args.packages = []
    else:
        parsed_args.packages = set(parsed_args.packages.split(","))

    tasks = []
    for package in parsed_args.packages:
        if package in packages:
            tasks.append(fetch_package(package, parsed_args.output))
        else:
            raise Exception(f"unknown package '{package}'")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        TimeElapsedColumn(),
        transient=True,
    ) as progress:
        progress.add_task("Fetching packages...")
        await gather(*tasks)

    if parsed_args.readme:
        log.info("[b]Updating README")
        readme.main()


def main(*args: Any, **kwargs: Any) -> None:
    run(async_main(*args, **kwargs))


if __name__ == "__main__":
    main()
