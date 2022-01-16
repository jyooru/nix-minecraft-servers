{ callPackage, lib, javaPackages }:

let
  latestVersion = versions: lib.last (builtins.sort lib.versionOlder (builtins.attrNames versions));
  escapeVersion = builtins.replaceStrings [ "." ] [ "_" ];

  getJavaVersion = v: (builtins.getAttr "openjdk${toString v}" javaPackages.compiler).headless;


  # airplane =
  #   let
  #     versions = lib.importJSON ./airplane/sources.json;
  #     packages = lib.mapAttrs'
  #       (version: value: {
  #         name = "airplane_${escapeVersion version}";
  #         value = callPackage ./airplane {
  #           inherit (value) version build url sha256;

  #         };
  #       })
  #       versions;
  #   in
  #   packages;


  paper =
    let
      versions = lib.importJSON ./paper/sources.json;
      packages = lib.mapAttrs'
        (version: value: {
          name = "paper_${escapeVersion version}";
          value = callPackage ./paper {
            inherit (value) version build url sha256;
          };
        })
        versions;
    in
    packages // { paper = builtins.getAttr "paper_${escapeVersion (latestVersion (lib.importJSON ./paper/sources.json))}" packages; };


  purpur =
    let
      versions = lib.importJSON ./purpur/sources.json;
      packages = lib.mapAttrs'
        (version: value: {
          name = "purpur_${escapeVersion version}";
          value = callPackage ./purpur {
            inherit (value) version build url sha256;
          };
        })
        versions;
    in
    packages // { purpur = builtins.getAttr "purpur_${escapeVersion (latestVersion (lib.importJSON ./purpur/sources.json))}" packages; };

  vanilla =
    let
      versions = lib.importJSON ./vanilla/sources.json;

      packages = lib.mapAttrs'
        (version: value: {
          name = "vanilla_${escapeVersion version}";
          value = callPackage ./vanilla {
            inherit (value) version url sha1;
            jre_headless = getJavaVersion (if value.javaVersion == null then 8 else value.javaVersion); # versions <= 1.6 will default to 8
          };
        })
        versions;
    in
    packages // { vanilla = builtins.getAttr "vanilla_${escapeVersion (latestVersion (lib.importJSON ./vanilla/sources.json))}" packages; };

  velocity =
    let
      versions = lib.importJSON ./velocity/sources.json;
      packages = lib.mapAttrs'
        (version: value: {
          name = "velocity_${escapeVersion version}";
          value = callPackage ./velocity {
            inherit (value) version build url sha256;
          };
        })
        versions;
    in
    packages // { velocity = builtins.getAttr "velocity_${escapeVersion (latestVersion (lib.importJSON ./velocity/sources.json))}" packages; };

  waterfall =
    let
      versions = lib.importJSON ./waterfall/sources.json;
      packages = lib.mapAttrs'
        (version: value: {
          name = "waterfall_${escapeVersion version}";
          value = callPackage ./waterfall {
            inherit (value) version build url sha256;
          };
        })
        versions;
    in
    packages // { waterfall = builtins.getAttr "waterfall_${escapeVersion (latestVersion (lib.importJSON ./waterfall/sources.json))}" packages; };

in
# airplane //
paper // purpur // vanilla // velocity // waterfall
