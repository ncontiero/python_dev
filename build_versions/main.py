import argparse
import logging
from typing import cast

from build_versions.ci_matrix import generate_matrix
from build_versions.dockerfiles import render_dockerfile_with_context
from build_versions.logger import init_logging
from build_versions.versions import load_versions

logger = logging.getLogger("dpn")


class CLIArgs(argparse.Namespace):
    ci_matrix: bool
    dockerfile_with_context: str
    verbose: bool


def main(args: CLIArgs) -> None:
    if args.dockerfile_with_context:
        render_dockerfile_with_context(args.dockerfile_with_context)
        return

    if args.ci_matrix:
        current_versions = load_versions()
        generate_matrix(current_versions)


def parse_args() -> CLIArgs:
    parser = argparse.ArgumentParser(usage="Build Python docker images")
    parser.add_argument("--ci-matrix", action="store_true", help="Generate CI build matrix")
    parser.add_argument("--dockerfile-with-context", default="", help="Render a dockerfile based on version config")
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging")

    return cast("CLIArgs", parser.parse_args())


if __name__ == "__main__":
    args = parse_args()
    init_logging(args.verbose)
    main(args)
