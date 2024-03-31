import dataclasses
import json
import logging
import os
from pathlib import Path

from build_versions.versions import BuildVersion

CI_EVENT_SCHEDULED = "scheduled"

logger = logging.getLogger("dpn")

GITHUB_OUTPUT = os.getenv("GITHUB_OUTPUT", "")


def _github_action_set_output(key: str, value: str) -> None:
    """Write
    https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#setting-an-output-parameter
    """
    with Path(GITHUB_OUTPUT).open("a") as fp:
        fp.write(f"{key}={value}")


def generate_matrix(versions: list[BuildVersion]) -> None:
    matrix = json.dumps({"include": [dataclasses.asdict(ver) for ver in versions]}) if versions else ""
    _github_action_set_output("MATRIX", matrix)
    logger.info("\n# Build versions:")
    logger.info("Nothing" if not versions else "\n".join(version.key for version in versions))
