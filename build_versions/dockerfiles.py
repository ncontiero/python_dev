import dataclasses
import datetime
import json
import logging
from typing import TYPE_CHECKING, Any

from jinja2 import Environment, FileSystemLoader, select_autoescape

from build_versions.constants import DOCKERFILES_PATH
from build_versions.versions import BuildVersion

if TYPE_CHECKING:
    from collections.abc import Mapping

logger = logging.getLogger("dpn")

env = Environment(loader=FileSystemLoader("./templates"), autoescape=select_autoescape())


def _render_template(template_name: str, context: Mapping[str, Any]) -> str:
    template = env.get_template(template_name)
    return template.render(context)


def render_dockerfile(version: BuildVersion) -> str:
    distro = "debian"

    context = dataclasses.asdict(version) | {
        "now": datetime.datetime.now(datetime.UTC).isoformat()[:-7],
        "distro": version.distro,
    }

    return _render_template(f"{distro}.Dockerfile", context)


def render_dockerfile_with_context(config_json: str) -> None:
    version = BuildVersion(**json.loads(config_json))

    dockerfile = render_dockerfile(version)

    filename = f"{version.key}.Dockerfile"
    logger.debug(f"Writing {filename}")
    if not DOCKERFILES_PATH.exists():
        DOCKERFILES_PATH.mkdir()

    dockerfile_path = DOCKERFILES_PATH / filename
    dockerfile_path.write_text(dockerfile)
