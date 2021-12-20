from typing import List
from jenkins import Jenkins


def last_successful_build() -> int:
    server = Jenkins("https://hub.spigotmc.org/jenkins/")
    job_info = server.get_job_info("BuildTools")
    last_successful_build: int = job_info["last_successful_build"]["number"]
    return last_successful_build


def get_jar_url(build: int) -> str:
    return f"https://hub.spigotmc.org/jenkins/job/BuildTools/{build}/artifact/target/BuildTools.jar"
