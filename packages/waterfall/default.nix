{ lib, stdenvNoCC, fetchurl, bash, jre, version, build, url, sha256 }:
let
  jar = fetchurl { inherit url sha256; };
in
stdenvNoCC.mkDerivation {
  pname = "waterfall";
  version = "${version}-${toString build}";

  preferLocalBuild = true;

  dontUnpack = true;
  dontConfigure = true;

  buildPhase = ''
    cat > waterfall << EOF
    #!${bash}/bin/sh
    exec ${jre}/bin/java \$@ -jar $out/share/waterfall/waterfall.jar
  '';

  installPhase = ''
    install -Dm444 ${jar} $out/share/waterfall/waterfall.jar
    install -Dm555 -t $out/bin waterfall
  '';

  meta = {
    description = "BungeeCord fork that aims to improve performance and stability";
    homepage = "https://papermc.io/";
    license = lib.licenses.mit;
    platforms = lib.platforms.unix;
    maintainers = with lib.maintainers; [ jyooru ];
  };
}
