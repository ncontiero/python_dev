import dataclasses
import json
import re

import httpx

from .constants import DOCKERHUB_API_URL, VERSIONS_PATH
from .logger import logger
from .versions import BuildVersion, load_versions


def fetch_latest_patch_versions(minor_versions: set[str], distros: list[str]) -> dict[str, dict[str, str]]:
    """
    Returns a dict mapping minor_version -> { distro -> full_version }
    """
    latest_versions: dict[str, dict[str, str]] = {m: {} for m in minor_versions}
    for minor_version in minor_versions:
        url = f"{DOCKERHUB_API_URL}?page_size=100&name={minor_version}"
        response = httpx.get(url)
        response.raise_for_status()
        results = response.json().get("results", [])

        for distro in distros:
            pattern = re.compile(rf"^{re.escape(minor_version)}\.(\d+)-slim-{re.escape(distro)}$")
            max_patch = -1
            full_version = None

            for tag in results:
                name = tag["name"]
                if match := pattern.match(name):
                    patch = int(match.group(1))
                    if patch > max_patch:
                        max_patch = patch
                        full_version = f"{minor_version}.{patch}"

            if full_version:
                latest_versions[minor_version][distro] = full_version
            else:
                logger.warning(f"No version found for {minor_version}-slim-{distro}")

    return latest_versions


def generate_new_versions() -> list[BuildVersion]:
    current_versions = load_versions()
    # Extract unique minor versions and distros from current versions
    minor_versions = set()
    distros = set()

    for v in current_versions:
        if match := re.match(r"^(\d+\.\d+)", v.python_version):
            minor_versions.add(match.group(1))
        distros.add(v.distro)

    logger.info("Fetching latest patch versions from Docker Hub...")
    latest_patches = fetch_latest_patch_versions(minor_versions, list(distros))

    new_versions = []
    has_changes = False

    for v in current_versions:
        match = re.match(r"^(\d+\.\d+)", v.python_version)
        if not match:
            new_versions.append(dataclasses.replace(v))
            continue

        minor = match.group(1)
        distro = v.distro

        latest_patch = latest_patches.get(minor, {}).get(distro)
        if not latest_patch or latest_patch == v.python_version:
            new_versions.append(dataclasses.replace(v))
            continue

        old_version = v.python_version
        new_v = dataclasses.replace(
            v,
            python_version=latest_patch,
            key=v.key.replace(old_version, latest_patch),
            python_image=v.python_image.replace(old_version, latest_patch),
        )
        new_versions.append(new_v)
        has_changes = True

    return new_versions if has_changes else []


def update_readme(versions: list[BuildVersion]) -> None:
    readme_path = VERSIONS_PATH.parent / "README.md"
    if not readme_path.exists():
        return

    content = readme_path.read_text()
    start_marker = "<!-- TAGS_START -->"
    end_marker = "<!-- TAGS_END -->"

    if start_marker not in content or end_marker not in content:
        logger.warning("Tags markers not found in README.md")
        return

    # Generate table
    table_lines = [
        "| Tag                      | Python version | Distro        |",
        "| ------------------------ | -------------- | ------------- |",
    ]
    for v in versions:
        if v.key != "latest" and not v.key.startswith("slim-"):
            tag_col = f"`{v.key}`"
            table_lines.append(f"| {tag_col:<24} | {v.python_version:<14} | {v.distro:<13} |")
    table_content = "\n".join(table_lines)

    pattern = re.compile(rf"{re.escape(start_marker)}.*?{re.escape(end_marker)}", re.DOTALL)
    new_content = pattern.sub(f"{start_marker}\n{table_content}\n{end_marker}", content)

    readme_path.write_text(new_content)


def update_versions() -> None:
    logger.info("Checking for version updates...")
    new_versions = generate_new_versions()

    if not new_versions:
        logger.info("Versions are up to date.")
        return

    new_dicts = [dataclasses.asdict(v) for v in new_versions]

    logger.info("Updating versions.json...")
    with VERSIONS_PATH.open("w") as fp:
        json.dump({"versions": new_dicts}, fp, indent=2)
        fp.write("\n")

    logger.info("Update complete.")
