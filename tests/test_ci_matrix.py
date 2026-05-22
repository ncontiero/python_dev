import json
import logging
from typing import TYPE_CHECKING

from python_dev.ci_matrix import _github_action_set_output, generate_matrix
from python_dev.versions import BuildVersion

if TYPE_CHECKING:
    from pathlib import Path

    import pytest
    from pytest_mock import MockerFixture


def test_github_action_set_output_with_env(mocker: MockerFixture, tmp_path: Path) -> None:
    output_file = tmp_path / "github_output"
    mocker.patch("python_dev.ci_matrix.GITHUB_OUTPUT", str(output_file))

    _github_action_set_output("MATRIX", "{}")

    assert output_file.read_text() == "MATRIX={}\n"


def test_github_action_set_output_without_env(mocker: MockerFixture, caplog: pytest.LogCaptureFixture) -> None:
    mocker.patch("python_dev.ci_matrix.GITHUB_OUTPUT", "")

    with caplog.at_level(logging.WARNING):
        _github_action_set_output("MATRIX", "{}")

    assert "GITHUB_OUTPUT is not set. Would have written: MATRIX={}" in caplog.text


def test_generate_matrix(mocker: MockerFixture) -> None:
    mock_set_output = mocker.patch("python_dev.ci_matrix._github_action_set_output")

    versions = [
        BuildVersion(
            key="latest",
            python_version="3.14.5",
            python_image="slim-trixie",
            distro="trixie",
            platforms=["linux/amd64"],
        ),
    ]

    generate_matrix(versions)

    expected_matrix = json.dumps(
        {
            "include": [
                {
                    "key": "latest",
                    "python_version": "3.14.5",
                    "python_image": "slim-trixie",
                    "distro": "trixie",
                    "platforms": ["linux/amd64"],
                },
            ],
        },
    )
    mock_set_output.assert_called_once_with("MATRIX", expected_matrix)
