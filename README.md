# Python Dev <img src="https://raw.githubusercontent.com/docker-library/docs/01c12653951b2fe592c1f93a13b4e289ada0e3a1/python/logo.png" alt="Python Image" width="30px" />

[![Build Status](https://img.shields.io/github/actions/workflow/status/dkshs/python_dev/build.yml?branch=master)](https://github.com/dkshs/python_dev/actions/workflows/build.yml?query=branch%3Amaster)
[![Docker Pulls](https://img.shields.io/docker/pulls/dkshs/python_dev?style=flat-square&color=7c3aed)](https://hub.docker.com/r/dkshs/python_dev)

An Python image with [uv](https://github.com/astral-sh/uv), zsh, [Oh My Zsh](https://ohmyz.sh/), git, gpg, gnupg, gpg-agent, socat, curl, wget, fonts-powerline; using theme [PowerLevel10k](https://github.com/romkatv/powerlevel10k) and plugins: git, git-flow, [fast-syntax-highlighting](https://github.com/zdharma-continuum/fast-syntax-highlighting), [zsh-autosuggestions](https://github.com/zsh-users/zsh-autosuggestions), [zsh-completions](https://github.com/zsh-users/zsh-completions).

## 🏷 Tags

To use a specific combination of Python see the following table of available image tags.

| Tag                     | Python version | Distro        |
| ----------------------- | -------------- | ------------- |
| `3.13.0-slim-bookworm`  | 3.13.0         | slim-bookworm |
| `3.13.0-slim-bullseye`  | 3.13.0         | slim-bullseye |
| `3.12.7-slim-bookworm`  | 3.12.7         | slim-bookworm |
| `3.12.7-slim-bullseye`  | 3.12.7         | slim-bullseye |
| `3.11.10-slim-bookworm` | 3.11.10        | slim-bookworm |
| `3.11.10-slim-bullseye` | 3.11.10        | slim-bullseye |
| `3.10.15-slim-bookworm` | 3.10.15        | slim-bookworm |
| `3.10.15-slim-bullseye` | 3.10.15        | slim-bullseye |
| `3.9.20-slim-bookworm`  | 3.9.20         | slim-bookworm |
| `3.9.20-slim-bullseye`  | 3.9.20         | slim-bullseye |

[See more](https://hub.docker.com/r/dkshs/python_dev/tags)

## Supported versions

| Python version | Start      | End     |
| -------------- | ---------- | ------- |
| 3.13           | 2024-10-07 | 2029-10 |
| 3.12           | 2023-10-02 | 2028-10 |
| 3.11           | 2022-10-24 | 2027-10 |
| 3.10           | 2021-10-04 | 2026-10 |
| 3.9            | 2020-10-05 | 2025-10 |

Versions are kept up to date using official sources. For Python we scrape the _Supported Versions_ table at [devguide.python.org/versions](https://devguide.python.org/versions/#supported-versions).

## How to use this image

### Create a Dockerfile in your Python app project

```dockerfile
FROM dkshs/python_dev:latest

USER ${USERNAME}

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=${USERNAME}:${USERNAME} . .
```

You can then build and run the Docker image:

```bash
docker build -t my-python-app .
docker run -it --rm my-python-app
```

### Run a single Python script

For many simple, single file projects, you may find it inconvenient to write a complete Dockerfile. In such cases, you can run a Python script by using the Python Docker image directly:

```bash
docker run -it --rm -v "$PWD":/home/dev-user/app -u dev-user dkshs/python_dev
```

All images have a default user `dev-user` with uid 1000 and gid 1000.

## Disclaimer

> This image is intended for development use only. Use it at your own risk!

## License

This project is under the [MIT](/LICENSE) license.
