{ callPackage, lib }:

with lib;

let
  cleanVersion = replaceStrings
    ([
      " Pre-Release "
      "."
      "-"
      " "
    ] ++ upperChars)
    ([
      "-pre"
      "_"
      "_"
      "_"
    ] ++ lowerChars);

  fullVersion = version:
    if (length (splitVersion version)) >= 3
    then version
    else fullVersion "${version}.0";

  cleanSourcesVersions = map (source:
    source // {
      version = cleanVersion (fullVersion source.version);
    }
  );

  mapAliases = aliases: packages:
    packages // (
      mapAttrs (_: value: getAttr value packages) aliases
    );

  importPackage = package:
    let
      sources = cleanSourcesVersions
        (importJSON (./. + "/${package}/sources.json"));
    in
    listToAttrs (map
      (source: {
        name = "${package}_${source.version}";
        value = callPackage (./. + "/${package}") source;
      })
      sources
    );

  importPackages = packages:
    foldr (a: b: a // b) { }
      (map importPackage packages);
in

mapAliases
  (importJSON ./aliases.json)
  (importPackages [
    "paper"
    "purpur"
    "vanilla"
    "velocity"
    "waterfall"
  ])
