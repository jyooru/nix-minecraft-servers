from typing import List
from jenkins import Jenkins
from .common import get
from bs4 import BeautifulSoup


def last_successful_build() -> int:
    server = Jenkins("https://hub.spigotmc.org/jenkins/")
    job_info = server.get_job_info("BuildTools")
    last_successful_build: int = job_info["last_successful_build"]["number"]
    return last_successful_build


def get_jar_url(build: int) -> str:
    return f"https://hub.spigotmc.org/jenkins/job/BuildTools/{build}/artifact/target/BuildTools.jar"


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
