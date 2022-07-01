{ lib, stdenvNoCC, fetchurl, bash, jre, version, build, url, sha256 }:
let
  jar = fetchurl { inherit url sha256; };
in
stdenvNoCC.mkDerivation {
  pname = "papermc";
  version = "${version}-${toString build}";

  preferLocalBuild = true;

  dontUnpack = true;
  dontConfigure = true;

  buildPhase = ''
    cat > minecraft-server << EOF
    #!${bash}/bin/sh
    exec ${jre}/bin/java \$@ -jar $out/share/papermc/papermc.jar nogui
  '';

  installPhase = ''
    install -Dm444 ${jar} $out/share/papermc/papermc.jar
    install -Dm555 -t $out/bin minecraft-server
  '';

  meta = {
    description = "High-performance Minecraft Server";
    homepage = "https://papermc.io/";
    license = lib.licenses.gpl3Only;
    platforms = lib.platforms.unix;
    maintainers = with lib.maintainers; [ aaronjanse neonfuz ];
  };
}
