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
        "-v",
        "--verbose",
        action="store_true",
        help="increase output verbosity",
    )
    if len(args) == 0:
        return parser.parse_args()
    else:
        return parser.parse_args(args)


def main() -> None:
    parsed_args = parse_args()
    if parsed_args.verbose:
        getLogger().setLevel("DEBUG")

    for name, module in packages.items():
        log.info(f"[b]Fetching versions for {name.title()}")
        module.main()

    log.info("f[b]Updating README")
    readme.main()


if __name__ == "__main__":
    main()
