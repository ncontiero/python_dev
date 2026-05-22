import json
from typing import TYPE_CHECKING

from python_dev.update import fetch_latest_patch_versions, generate_new_versions, update_readme, update_versions
from python_dev.versions import BuildVersion

if TYPE_CHECKING:
    from pathlib import Path

    from pytest_mock import MockerFixture


def test_fetch_latest_patch_versions(mocker: MockerFixture) -> None:
    mock_get = mocker.patch("httpx.get")
    mock_response = mocker.Mock()
    mock_response.json.return_value = {
        "results": [
            {"name": "3.14.5-slim-bookworm"},
            {"name": "3.14.4-slim-bookworm"},
            {"name": "3.14.5-slim-trixie"},
        ],
    }
    mock_get.return_value = mock_response

    result = fetch_latest_patch_versions({"3.14"}, ["bookworm", "trixie"])

    assert result == {
        "3.14": {
            "bookworm": "3.14.5",
            "trixie": "3.14.5",
        },
    }


def test_generate_new_versions(mocker: MockerFixture) -> None:
    mocker.patch(
        "python_dev.update.load_versions",
        return_value=[
            BuildVersion("latest", "3.14.4", "slim-trixie", "trixie", ["linux/amd64"]),
            BuildVersion("slim-trixie", "3.14.4", "slim-trixie", "trixie", ["linux/amd64"]),
            BuildVersion("3.14.4-slim-trixie", "3.14.4", "3.14.4-slim-trixie", "trixie", ["linux/amd64"]),
        ],
    )

    mocker.patch(
        "python_dev.update.fetch_latest_patch_versions",
        return_value={
            "3.14": {
                "trixie": "3.14.5",
            },
        },
    )

    new_versions = generate_new_versions()

    assert len(new_versions) == 3
    keys = {v.key for v in new_versions}
    assert "latest" in keys
    assert "slim-trixie" in keys
    assert "3.14.5-slim-trixie" in keys

    for v in new_versions:
        assert v.python_version == "3.14.5"


def test_update_readme(mocker: MockerFixture, tmp_path: Path) -> None:
    # Use tmp_path to mock VERSIONS_PATH parent for README.md
    readme_path = tmp_path / "README.md"
    readme_path.write_text("Header\n<!-- TAGS_START -->\nold content\n<!-- TAGS_END -->\nFooter")

    mocker.patch("python_dev.update.VERSIONS_PATH", tmp_path / "versions.json")

    versions = [
        BuildVersion("latest", "3.14.5", "slim-trixie", "trixie", []),
        BuildVersion("3.14.5-slim-trixie", "3.14.5", "3.14.5-slim-trixie", "trixie", []),
    ]

    update_readme(versions)

    new_content = readme_path.read_text()
    assert "Header" in new_content
    assert "Footer" in new_content
    assert "`3.14.5-slim-trixie`" in new_content
    assert "latest" not in new_content  # "latest" key is skipped in table per logic


def test_update_versions_no_changes(mocker: MockerFixture) -> None:
    mocker.patch("python_dev.update.generate_new_versions", return_value=[])
    mock_logger = mocker.patch("python_dev.update.logger")

    update_versions()

    mock_logger.info.assert_any_call("Versions are up to date.")


def test_update_versions_with_changes(mocker: MockerFixture, tmp_path: Path) -> None:
    new_version = BuildVersion("latest", "3.15.0", "slim-trixie", "trixie", [])
    mocker.patch("python_dev.update.generate_new_versions", return_value=[new_version])

    versions_path = tmp_path / "versions.json"
    mocker.patch("python_dev.update.VERSIONS_PATH", versions_path)
    mock_logger = mocker.patch("python_dev.update.logger")

    update_versions()

    mock_logger.info.assert_any_call("Updating versions.json...")

    data = json.loads(versions_path.read_text())
    assert data["versions"][0]["python_version"] == "3.15.0"
