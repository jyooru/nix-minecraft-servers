{ lib, stdenv, fetchurl, bash, jre, version, build, url, sha256 }:
let
  jar = fetchurl { inherit url sha256; };
in
stdenv.mkDerivation {
  pname = "airplane";
  version = "${version}-${toString build}";

  preferLocalBuild = true;

  dontUnpack = true;
  dontConfigure = true;

  installPhase = ''
    mkdir -p $out/bin $out/lib/minecraft
    cp -v ${jar} $out/lib/minecraft/launcher-airplane.jar
    cat > $out/bin/minecraft-server << EOF
    #!/bin/sh
    exec ${jre}/bin/java \$@ -jar $out/lib/minecraft/launcher-airplane.jar nogui
    EOF
    chmod +x $out/bin/minecraft-server
  '';

  meta = {
    description = "An optimized 1.17.1 Paper fork";
    homepage = "https://airplane.gg/";
    license = lib.licenses.gpl3Only;
    platforms = lib.platforms.unix;
    maintainers = with lib.maintainers; [ jyooru ];
  };
}
