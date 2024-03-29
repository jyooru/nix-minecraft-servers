{
  description = "Minecraft server packages";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
    utils.url = "github:gytis-ivaskevicius/flake-utils-plus";
  };

  outputs = { self, nixpkgs, utils } @ inputs:
    nixpkgs.lib.warn "nix-minecraft-servers is no longer being maintained. Please use https://github.com/Infinidoge/nix-minecraft" (
      utils.lib.mkFlake {
        inherit self inputs;

        outputsBuilder = channels:
          let pkgs = channels.nixpkgs; in
          with pkgs;
          {
            packages = (self.overlays.default pkgs pkgs).minecraftServers // rec {
              default = minecraft-servers;
              minecraft-servers = callPackage ./ci { };
            };
          };

        overlays = rec {
          default = nix-minecraft-servers;
          nix-minecraft-servers = final: prev: {
            minecraftServers = import ./packages {
              inherit (final) callPackage lib;
            };
          };
        };

        overlay = nixpkgs.lib.warn "the nix-minecraft-servers overlay has been renamed from 'overlay' to 'overlays.default'" self.overlays.default;
      }
    );
}
