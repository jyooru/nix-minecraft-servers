import argparse
from logging import getLogger
from typing import List

from . import packages, readme


log = getLogger(__name__)


def parse_args(args: List[str] = []) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="minecraft-servers",
        description="Automatically updated Minecraft servers",
    )
    parser.add_argument(
        "-p",
        "--packages",
        type=str,
        help="comma seperated string of packages to fetch",
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


def main(args: List[str] = []) -> None:
    parsed_args = parse_args(args)

    if parsed_args.verbose:
        getLogger().setLevel("DEBUG")
    if parsed_args.packages is None:
        parsed_args.packages = set(packages.keys())
    else:
        parsed_args.packages = set(parsed_args.packages.split(","))

    for package in parsed_args.packages:
        if package in packages:
            log.info(f"[b]Fetching versions for {package.title()}")
            packages[package].main()
        else:
            raise Exception(f"unknown package '{package}'")

    log.info("[b]Updating README")
    readme.main()


if __name__ == "__main__":
    main()
