from logging import getLogger

from . import pkgs


log = getLogger(__name__)


def main() -> None:
    for pkg in pkgs.values():
        pkg.main()


if __name__ == "__main__":
    main()
