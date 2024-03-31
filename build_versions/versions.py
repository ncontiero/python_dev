import json
from dataclasses import dataclass

from build_versions.constants import VERSIONS_PATH


@dataclass
class BuildVersion:
    """A docker image build for a specific combination of python versions"""

    key: str
    python: str
    python_canonical: str
    python_image: str
    distro: str
    platforms: list[str]


def load_versions() -> list[BuildVersion]:
    with VERSIONS_PATH.open() as fp:
        version_dicts = json.load(fp)["versions"]
        return [BuildVersion(**version) for version in version_dicts]
