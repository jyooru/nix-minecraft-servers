{ callPackage, lib }:

with lib;

let
  escapeVersion = replaceStrings [ "." ] [ "_" ];
  unescapeVersion = replaceStrings [ "_" ] [ "." ];

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
          sources = importJSON (./. + "/${package}/sources.json");
          packages = listToAttrs (map
            (source: {
              name = fullVersion source.version;
              value = callPackage (./. + "/${package}") source;
            })
            sources
          );
        in
        mapAttrs'
          (name: value: {
            name = "${package}_${escapeVersion name}";
            inherit value;
          })
          packages)
      allPackages);
in

packages // (mapAttrs (_: v: getAttr v packages) aliases)
