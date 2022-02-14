{
  description = "Minecraft server packages";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem
      (system:
        let
          pkgs = import nixpkgs { config.allowUnfree = true; inherit system; };
        in
        with pkgs;
        rec {
          devShell = (poetry2nix.mkPoetryEnv { projectDir = ./ci; }).env;

          overlay = (final: prev: { minecraftServers = packages; });
          defaultPackage = poetry2nix.mkPoetryApplication { projectDir = ./ci; };
          packages = import ./packages { inherit (pkgs) callPackage lib; };
        }
      );
}
