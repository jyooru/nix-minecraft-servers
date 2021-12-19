{
  description = "Minecraft server packages";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem
      (system:
        let pkgs = import nixpkgs { inherit system; }; in
        with pkgs;
        rec {
          devShell = pkgs.mkShell {
            packages = [ python3 ] ++ (with python3Packages; [ black dataclasses-json flake8 isort requests mypy ]);
          };

          packages = import ./pkgs { inherit (pkgs) callPackage lib javaPackages; };
        }
      );
}
