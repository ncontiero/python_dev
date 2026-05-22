from pathlib import Path

# Paths
BASE_PATH = Path(__file__).parent.parent.parent
VERSIONS_PATH = BASE_PATH / "versions.json"
DOCKERFILES_PATH = BASE_PATH / "dockerfiles"

DEFAULT_PLATFORMS = ["linux/amd64", "linux/arm64"]
DEFAULT_DISTRO = "trixie"
DISTROS = ["trixie", "bookworm"]

BASE_MAPPING = {
    "bookworm": "debian",
    "trixie": "debian",
}

DOCKERHUB_API_URL = "https://hub.docker.com/v2/repositories/library/python/tags/"
