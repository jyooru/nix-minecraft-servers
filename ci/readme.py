import json
import subprocess


def find_line(lines: list[str], string: str) -> int:
    for index, line in enumerate(lines):
        if line.replace("\n", "") == string:
            return index
    raise Exception(f"Could not find line: {string}")


def get_packages() -> dict[str, dict[str, str]]:
    output = json.loads(
        subprocess.check_output(["nix", "search", ".", "--json"]).decode("UTF-8")
    )
    return {key.split(".")[2]: value for key, value in output.items()}


def main():
    with open("README.md") as file:
        old_readme = file.readlines()
    new_readme = []
    start = find_line(old_readme, "<!-- ci.readme start -->") + 2
    end = find_line(old_readme[start:], "<!-- ci.readme end -->") + start - 1

    packages = {key: value["version"] for key, value in get_packages().items()}

    new_readme += old_readme[:start]
    new_readme.append("| Name |Latest Version |\n")
    new_readme.append("| --- | --- |\n")
    new_readme += [
        f"| {package} | {version} |\n"
        for package, version in packages.items()
        if "_" not in package 
    ]
    new_readme.append("<details>\n")
    new_readme.append("<summary><b>All versions available</b></summary>\n")
    new_readme.append("<table>\n")
    new_readme.append("<tr><th>Name</th><th>Version</th></tr>\n")
    new_readme += [
        f"<tr><td>{package}</td><td>{version}</td></tr>\n"
        for package, version in packages.items()
    ]
    new_readme.append("</table>\n")
    new_readme.append("</details>\n")
    new_readme += old_readme[end:]

    with open("README.md", "w") as file:
        file.writelines(new_readme)

    subprocess.check_call(["prettier", "-w", "README.md"])


if __name__ == "__main__":
    main()
