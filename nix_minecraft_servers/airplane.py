from typing import Dict, List, Union
from jenkins import Jenkins
import json
from logging import getLogger


log = getLogger(__name__)


def last_successful_build() -> int:
    server = Jenkins("https://ci.tivy.ca/")
    job_info = server.get_job_info("Airplane-1.17")
    last_successful_build: int = job_info["lastSuccessfulBuild"]["number"]
    return last_successful_build


def generate() -> Dict[str, Union[int, List[str]]]:
    return {"latest": {"build": last_successful_build(), "version": "1.17.1"}}


def main() -> None:
    with open("pkgs/airplane.json", "w") as file:
        data = generate()
        log.info(f"[b]Found {len(data.keys())} versions for Airplane")
        json.dump(data, file, indent=2)
        file.write("\n")


if __name__ == "__main__":
    main()
