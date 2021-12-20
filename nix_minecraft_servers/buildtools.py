from typing import Dict, List, Union
from jenkins import Jenkins
from .common import get
from bs4 import BeautifulSoup
import json
from logging import getLogger


log = getLogger(__name__)


def last_successful_build() -> int:
    server = Jenkins("https://hub.spigotmc.org/jenkins/")
    job_info = server.get_job_info("BuildTools")
    last_successful_build: int = job_info["lastSuccessfulBuild"]["number"]
    return last_successful_build


def get_versions() -> List[str]:
    soup = BeautifulSoup(
        get("https://hub.spigotmc.org/versions/").content, "html.parser"
    )
    links = [link.get("href") for link in soup.pre.find_all("a")]
    return [
        link.replace(".json", "")
        for link in links
        if link.startswith("1.") and link.endswith(".json")
    ]


def generate() -> Dict[str, Union[int, List[str]]]:
    return {"build": last_successful_build(), "revs": get_versions()}


def main() -> None:
    with open("pkgs/buildtools.json", "w") as file:
        data = generate()
        log.info(f"[b]Found {len(data['revs'])} versions for BuildTools")
        json.dump(data, file, indent=2)
        file.write("\n")


if __name__ == "__main__":
    main()
