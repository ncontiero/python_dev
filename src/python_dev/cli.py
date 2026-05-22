import argparse
from typing import Literal, cast

from .ci_matrix import generate_matrix
from .dockerfiles import render_dockerfile_with_context
from .update import update_versions
from .versions import load_versions


class CLIArgs(argparse.Namespace):
    command: Literal["update", "render-dockerfile", "ci-matrix"]
    dockerfile_with_context: str
    verbose: bool


def main(args: CLIArgs) -> None:
    if args.command == "update":
        update_versions()
    elif args.command == "render-dockerfile":
        render_dockerfile_with_context(args.dockerfile_with_context)
    elif args.command == "ci-matrix":
        current_versions = load_versions()
        generate_matrix(current_versions)


def parse_args() -> CLIArgs:
    parser = argparse.ArgumentParser(usage="Build Python docker images")
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging")

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("ci-matrix", help="Generate CI build matrix")
    subparsers.add_parser("update", help="Update versions.json based on Docker Hub")

    render_parser = subparsers.add_parser("render-dockerfile", help="Render a dockerfile based on version config")
    render_parser.add_argument("dockerfile_with_context", help="JSON string of the version config")

    return cast("CLIArgs", parser.parse_args())
