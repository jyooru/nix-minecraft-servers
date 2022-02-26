{ callPackage, lib }:

with lib;

let
  cleanVersion = s: toLower
    (replaceStrings
      [
        " Pre-Release "
        "."
        "-"
        " "
      ]
      [
        "-pre"
        "_"
        "_"
        "_"
      ]
      s);

  fullVersion = version:
    if (length (splitVersion version)) >= 3
    then version
    else fullVersion "${version}.0";

  aliases = importJSON ./aliases.json;
  insertAliases = attrs: mapAttrs (_: v: null);

  allPackages = [ "paper" "purpur" "vanilla" "velocity" "waterfall" ];
  packages = lib.foldr (a: b: a // b) { }
    (map
      (package:
        let
          sources = map
            (source:
              source // { version = cleanVersion (fullVersion source.version); }
            )
            (importJSON (./. + "/${package}/sources.json"));
          packages = listToAttrs (map
            (source: {
              name = source.version;
              value = callPackage (./. + "/${package}") source;
            })
            sources
          );
        in
        mapAttrs'
          (name: value: {
            name = "${package}_${name}";
            inherit value;
          })
          packages)
      allPackages);
in

packages // (mapAttrs (_: v: getAttr v packages) aliases)
