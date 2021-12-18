{ callPackage, lib, javaPackages }:

let
  latestVersion = versions: lib.last (builtins.sort lib.versionOlder (builtins.attrNames versions));
  escapeVersion = builtins.replaceStrings [ "." ] [ "_" ];

  getJavaVersion = v: (builtins.getAttr "openjdk${toString v}" javaPackages.compiler).headless;

  purpur =
    let
      versions = lib.importJSON ./purpur.json;
      packages = lib.mapAttrs'
        (version: value: {
          name = "purpur_${escapeVersion version}";
          value = callPackage ./purpur.nix {
            inherit (value) version build url sha256;
          };
        })
        versions;
    in
    packages // { purpur = builtins.getAttr "purpur_${escapeVersion (latestVersion (lib.importJSON ./purpur.json))}" packages; };

  vanilla =
    let
      versions = lib.importJSON ./vanilla.json;

      packages = lib.mapAttrs'
        (version: value: {
          name = "vanilla_${escapeVersion version}";
          value = callPackage ./vanilla.nix {
            inherit (value) version url sha1;
            jre_headless = getJavaVersion (if value.javaVersion == null then 8 else value.javaVersion); # versions <= 1.6 will default to 8
          };
        })
        versions;
    in
    packages // { vanilla = builtins.getAttr "vanilla_${escapeVersion (latestVersion (lib.importJSON ./vanilla.json))}" packages; };
in
purpur // vanilla
