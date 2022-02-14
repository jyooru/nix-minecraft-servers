from logging import getLogger

from . import packages, readme


log = getLogger(__name__)


def main() -> None:
    for name, module in packages.items():
        log.info(f"[b]Fetching versions for {name.title()}")
        module.main()

    log.info("f[b]Updating README")
    readme.main()


if __name__ == "__main__":
    main()
