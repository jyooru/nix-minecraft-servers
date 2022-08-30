# nix-minecraft-servers

This project contains all Minecraft server versions packaged for Nix.

# Usage

All packages are available through this flake's package set (`minecraft-servers.packages`) and overlay (`minecraft-servers.overlay`). To use them, add this repository to your flake inputs:

```nix
# flake.nix
{
  inputs = {
    minecraft-servers.url = "github:jyooru/nix-minecraft-servers";
  };
}
```

## Packages

All packages are available through this flake's package set:

```nix
# configuration.nix
{ inputs }:
{
  services.minecraft-server = {
    enable = true;
    eula = true;
    package = inputs.minecraft-server.vanilla_1_8_9;
  };
}
```

### Version Aliases

All major and minor version of all packages are aliased in such a way that you can:

- be more specific and lock a package to a specific version, such as the attribute `vanilla_1_8_9`
- be less specific and automatically choose the latest version of a range, such as the attribute `vanilla_1_8` which is the same as `vanilla_1_8_9`
- not be specific at all and just choose the latest version, such as `vanilla` which (at the time of writing) points to `vanilla_1_18_1`

All aliases always point to a release and will never point to a beta or snapshot.

## Overlay

The overlay overrides nixpkgs' `minecraftServers` attribute with this flake's `packages` attribute:

```nix
# configuration.nix
{ inputs, pkgs }:
{
  nixpkgs.overlays = [ inputs.minecraft-servers.overlays.default ];

  services.minecraft-server = {
    enable = true;
    eula = true;
    package = pkgs.minecraftServers.vanilla_1_8_9;
  };
}
```

# Packages

[![update](https://github.com/jyooru/nix-minecraft-servers/actions/workflows/update.yml/badge.svg?event=schedule)](https://github.com/jyooru/nix-minecraft-servers/actions/workflows/update.yml)

The latest version of each package is shown in the table below. To see all versions available, run `nix flake search github:jyooru/nix-minecraft-servers`. You can filter the search by appending your query on the end of the command.

<!-- minecraft-servers start -->

| Name      | Latest Version |
| --------- | -------------- |
| paper     | 1_19_2-135     |
| purpur    | 1_19_2-1770    |
| vanilla   | 1_19_2         |
| velocity  | 3_1_1-102      |
| waterfall | 1_19_0-504     |

<!-- minecraft-servers end -->

# Behind the scenes

This repository also contains a Python module in the [ci subdirectory](./ci) that contains the code to fetch all data needed for all packages and versions.

This python module is run daily by a [GitHub Actions workflow](./.github/workflows/update.yml) that then [commits the output](https://github.com/jyooru/nix-minecraft-servers/commits?author=github-actions%5Bbot%5D), [opens a PR](https://github.com/jyooru/nix-minecraft-servers/pulls?q=is%3Apr+chore%28packages%29%3A+update) and sets it to automatically merge if [all packages build](https://hercules-ci.com/github/jyooru/nix-minecraft-servers).

# License

See [LICENSE](LICENSE) for details.
