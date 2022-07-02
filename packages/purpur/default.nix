{ lib, stdenvNoCC, fetchurl, nixosTests, jre_headless, version, build, url, sha256 }:
stdenvNoCC.mkDerivation {
  pname = "purpur";
  version = "${version}-${toString build}";

  src = fetchurl { inherit url sha256; };

  preferLocalBuild = true;

  installPhase = ''
    mkdir -p $out/bin $out/lib/minecraft
    cp -v $src $out/lib/minecraft/server.jar
    cat > $out/bin/minecraft-server << EOF
    #!/bin/sh
    exec ${jre_headless}/bin/java \$@ -jar $out/lib/minecraft/server.jar nogui
    EOF
    chmod +x $out/bin/minecraft-server
  '';

  dontUnpack = true;

  passthru = {
    tests = { inherit (nixosTests) minecraft-server; };
  };

  meta = with lib; {
    description = "Purpur is a drop-in replacement for Paper servers designed for configurability, new fun and exciting gameplay features, and performance built on top of Airplane.";
    homepage = "https://purpurmc.org/";
    license = licenses.mit;
    platforms = platforms.unix;
    maintainers = with maintainers; [ jyooru ];
  };
}
