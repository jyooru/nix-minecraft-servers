{ callPackage, lib, javaPackages }:
# if you add more versions make sure to add to all-packages.nix
let
  versions = lib.importJSON ./vanilla.json;

  latestVersion = lib.last (builtins.sort lib.versionOlder (builtins.attrNames versions));
  escapeVersion = builtins.replaceStrings [ "." ] [ "_" ];

  getJavaVersion = v: (builtins.getAttr "openjdk${toString v}" javaPackages.compiler).headless;

  packages = lib.mapAttrs'
    (version: value: {
      name = "vanilla_${escapeVersion version}";
      value = callPackage ./derivation.nix {
        name = "vanilla";
        inherit (value) version url sha1;
        jre_headless = getJavaVersion (if value.javaVersion == null then 8 else value.javaVersion); # versions <= 1.6 will default to 8
      };
    })
    versions;
in
packages // {
  vanilla = builtins.getAttr "vanilla_${escapeVersion latestVersion}" packages;
}
