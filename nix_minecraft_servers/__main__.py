from logging import getLogger

from . import pkgs


log = getLogger(__name__)


def main() -> None:
    for name, module in pkgs.items():
        log.info(f"[b]Fetching versions for {name.title()}")
        module.main()


if __name__ == "__main__":
    main()
