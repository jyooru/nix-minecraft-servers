{ lib
, fetchFromGitHub
, python3
}:

python3.pkgs.buildPythonApplication rec {
  pname = "minecraft-servers";
  version = "0.1.0";
  format = "pyproject";

  src = ./.;

  nativeBuildInputs = with python3.pkgs; [
    poetry-core
  ];

  propagatedBuildInputs = with python3.pkgs; [
    dataclasses-json
    python-jenkins
    requests
    rich
    aiohttp
    semantic-version
    platformdirs
  ];

  pythonImportsCheck = [
    "minecraft_servers"
  ];

  meta = with lib; {
    description = "Automatically updated Minecraft servers";
    homepage = "https://github.com/jyooru/nix-minecraft-servers";
    license = licenses.mit;
    maintainers = with maintainers; [ jyooru ];
  };
}
