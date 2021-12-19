from .pkgs import pkgs


def main() -> None:
    for pkg in pkgs.values():
        pkg.main()


if __name__ == "__main__":
    main()
