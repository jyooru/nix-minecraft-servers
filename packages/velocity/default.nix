{ lib, stdenv, fetchurl, bash, jre, version, build, url, sha256 }:
let
  jar = fetchurl { inherit url sha256; };
in
stdenv.mkDerivation {
  pname = "velocity";
  version = "${version}-${toString build}";

  preferLocalBuild = true;

  dontUnpack = true;
  dontConfigure = true;

  buildPhase = ''
    cat > velocity << EOF
    #!${bash}/bin/sh
    exec ${jre}/bin/java \$@ -jar $out/share/velocity/velocity.jar
  '';

  installPhase = ''
    install -Dm444 ${jar} $out/share/velocity/velocity.jar
    install -Dm555 -t $out/bin velocity
  '';

  meta = {
    description = "Velocity is a next-generation Minecraft proxy focused on scalability and flexibility.";
    homepage = "https://velocitypowered.com/";
    license = lib.licenses.gpl3Only;
    platforms = lib.platforms.unix;
    maintainers = with lib.maintainers; [ jyooru ];
  };
}
