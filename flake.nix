{
  description = "Minecraft server packages";

  inputs = {
    flake-compat = { url = "github:edolstra/flake-compat"; flake = false; };
    flake-compat-ci.url = "github:hercules-ci/flake-compat-ci";
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem
      (system:
        let
          pkgs = import nixpkgs { inherit system; };
          requirements = with pkgs; [
            (python3.withPackages (ps: with ps; [ black dataclasses-json flake8 isort mypy python-jenkins requests rich types-requests ]))
          ];
        in
        with pkgs;
        rec {
          apps = {
            nix-minecraft-server = writeShellApplication {
              runtimeInputs = requirements;
              name = "nix-minecraft-server";
              text = "PYTHONPATH='${toString ./.}' python3 -m nix_minecraft_servers";
            };
          };
          defaultApp = apps.nix-minecraft-server;

          ciNix = {
            inherit devShell;
            packages = recurseIntoAttrs packages;
          };

          devShell = pkgs.mkShell { packages = requirements; };

          packages = import ./pkgs { inherit (pkgs) callPackage lib javaPackages; };
        }
      );
}
