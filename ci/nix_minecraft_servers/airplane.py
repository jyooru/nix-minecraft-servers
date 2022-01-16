import json
from logging import getLogger
from typing import Dict, List, Union

from jenkins import Jenkins

from .common import get_sha256


log = getLogger(__name__)


def last_successful_build() -> int:
    server = Jenkins("https://ci.tivy.ca/")
    job_info = server.get_job_info("Airplane-1.17")
    last_successful_build: int = job_info["lastSuccessfulBuild"]["number"]
    return last_successful_build


def generate() -> Dict[str, Dict[str, Union[int, List[str], str]]]:
    build = last_successful_build()
    url = f"https://ci.tivy.ca/job/Airplane-1.17/{build}/artifact/launcher-airplane.jar"
    return {
        "latest": {
            "build": build,
            "sha256": get_sha256(url),
            "url": url,
            "version": "1.17.1",
        }
    }


def main() -> None:
    with open("packages/airplane/sources.json", "w") as file:
        data = generate()
        log.info(f"[b]Found {len(data.keys())} versions for Airplane")
        json.dump(data, file, indent=2)
        file.write("\n")


if __name__ == "__main__":
    main()
