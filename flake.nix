{
  description = "Minecraft server packages";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
    utils.url = "github:gytis-ivaskevicius/flake-utils-plus";
  };

  outputs = { self, nixpkgs, utils, ... } @ inputs:
    utils.lib.mkFlake {
      inherit self inputs;

      channelsConfig.allowUnfree = true;

      outputsBuilder = channels:
        let pkgs = channels.nixpkgs; in
        with pkgs;
        {
          defaultPackage = poetry2nix.mkPoetryApplication { projectDir = ./ci; };

          devShell = (poetry2nix.mkPoetryEnv { projectDir = ./ci; }).env;

          packages = (self.overlay pkgs pkgs).minecraftServers;
        };

      overlay = final: prev: {
        minecraftServers = import ./packages {
          inherit (final) callPackage lib;
        };
      };
    };
}
