from typing import TYPE_CHECKING

from python_dev.dockerfiles import render_dockerfile
from python_dev.versions import BuildVersion

if TYPE_CHECKING:
    from pytest_mock import MockerFixture


def test_render_dockerfile(mocker: MockerFixture) -> None:
    mock_render = mocker.patch("python_dev.dockerfiles._render_template", return_value="Dockerfile content")

    version = BuildVersion(
        key="latest",
        python_version="3.14.5",
        python_image="slim-trixie",
        distro="trixie",
        platforms=["linux/amd64"],
    )

    result = render_dockerfile(version)

    assert result == "Dockerfile content"
    mock_render.assert_called_once()
    args, _ = mock_render.call_args

    # Assert it resolved trixie to debian base
    assert args[0] == "debian.Dockerfile"
    assert args[1]["python_version"] == "3.14.5"
    assert args[1]["distro"] == "trixie"
