{
  description = "Minecraft server packages";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem
      (system:
        let
          pkgs = import nixpkgs { inherit system; };
          requirements = with pkgs; [ python3 ] ++ (with python3Packages; [ black dataclasses-json flake8 isort mypy requests rich types-requests ]);
        in
        with pkgs;
        rec {
          apps = {
            run = writeShellApplication { runtimeInputs = requirements; name = "nix-minecraft-server-run"; text = "python3 -m nix_minecraft_servers"; };
          };
          defaultApp = apps.run;

          devShell = pkgs.mkShell {
            packages = requirements;
          };

          packages = import ./pkgs { inherit (pkgs) callPackage lib javaPackages; };
        }
      );
}
