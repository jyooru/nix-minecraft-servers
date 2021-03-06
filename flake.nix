{
  description = "Minecraft server packages";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
    utils.url = "github:gytis-ivaskevicius/flake-utils-plus";
  };

  outputs = { self, nixpkgs, utils } @ inputs:
    utils.lib.mkFlake {
      inherit self inputs;

      outputsBuilder = channels:
        let pkgs = channels.nixpkgs; in
        with pkgs;
        {
          devShells = rec {
            default = minecraft-servers;
            minecraft-servers = (poetry2nix.mkPoetryEnv { projectDir = ./ci; }).env;
          };

          packages = (self.overlays.default pkgs pkgs).minecraftServers // rec {
            default = minecraft-servers;
            minecraft-servers = poetry2nix.mkPoetryApplication { projectDir = ./ci; };
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
    };
}
