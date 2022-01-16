{ callPackage, lib }:

let
  inherit (builtins) attrNames getAttr replaceStrings sort;
  inherit (lib) importJSON last mapAttrs' versionOlder;

  escapeVersion = replaceStrings [ "." ] [ "_" ];
  latestVersion = versions: last (sort versionOlder (attrNames versions));

  # [ "airplane" ]
  allPackages = [ "paper" "purpur" "vanilla" "velocity" "waterfall" ];
in

lib.foldr (a: b: a // b) { }
  (map
    (package:
      let
        sources = importJSON (./. + "/${package}/sources.json");
        packages = mapAttrs'
          (version: source: {
            name = package + "_" + (escapeVersion version);
            value = callPackage (./. + "/${package}") source;
          })
          sources;
      in
      packages // { ${package} = getAttr (package + "_" + (escapeVersion (latestVersion sources))) packages; }
    )
    allPackages)
