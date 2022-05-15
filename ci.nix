with builtins;

let
  flake = getFlake (toString ./.);
  pkgs = import flake.inputs.nixpkgs {
    config = {
      allowUnfree = true;
      permittedInsecurePackages = [
        "openjdk-headless-16+36"
      ];
    };
  };
in

with flake.inputs.nixpkgs.lib;

{
  packages = recurseIntoAttrs
    ((flake.overlays.default pkgs pkgs).minecraftServers // rec {
      inherit (flake.packages.${currentSystem}) minecraft-servers;
    });
}
