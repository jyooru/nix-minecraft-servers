let
  inherit (builtins) currentSystem getFlake;
  inherit (flake) inputs;
  inherit (pkgs) lib;
  inherit (lib) recurseIntoAttrs;

  flake = getFlake (toString ./.);
  pkgs = import inputs.nixpkgs { inherit system; };
  system = currentSystem;
in
{
  defaultPackage = flake.defaultPackage.${system};
  packages = recurseIntoAttrs flake.packages.${system};
}
