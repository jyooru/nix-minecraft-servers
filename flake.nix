{
  description = "Minecraft server packages";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
  };

  outputs = { self, nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem
      (system:
        let
          pkgs = import nixpkgs { config.allowUnfree = true; inherit system; };
        in
        with pkgs;
        rec {
          defaultPackage = poetry2nix.mkPoetryApplication { projectDir = ./ci; };

          devShell = (poetry2nix.mkPoetryEnv { projectDir = ./ci; }).env;

          overlay = final: prev:
            {
              minecraftServers = import ./packages {
                inherit (final) callPackage lib;
              };
            };

          packages = (overlay pkgs pkgs).minecraftServers;
        }
      );
}
