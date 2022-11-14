# Python Dev <img src="https://raw.githubusercontent.com/docker-library/docs/01c12653951b2fe592c1f93a13b4e289ada0e3a1/python/logo.png" alt="Python Image" width="30px" />

An image with [Python 3.8.10-slim](https://hub.docker.com/layers/library/python/3.8.10-slim/images/sha256-dc50f1da4e2e0c8a6a53a342d11b7779bba81f0d668bdb2b9bbd68c647620fe4?context=explore), zsh, [Oh My Zsh](https://ohmyz.sh/), git, gpg, gnupg, gpg-agent, socat, curl, wget, fonts-powerline; using theme [PowerLevel10k](https://github.com/romkatv/powerlevel10k) and plugins: git, git-flow, [fast-syntax-highlighting](https://github.com/zdharma-continuum/fast-syntax-highlighting), [zsh-autosuggestions](https://github.com/zsh-users/zsh-autosuggestions), [zsh-completions](https://github.com/zsh-users/zsh-completions)

> The image already contains a code that makes the container stand up!

## How to use this image

### Create a Dockerfile in your Python app project

```dockerfile
FROM dkshs/python_dev:latest

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
```

You can then build and run the Docker image:

```bash
docker build -t my-python-app .
docker run -it --rm --name my-app-python my-python-app
```

### Run a single Python script

For many simple, single file projects, you may find it inconvenient to write a complete Dockerfile. In such cases, you can run a Python script by using the Python Docker image directly:

```bash
docker run -it --rm --name my-app-python -v "$PWD":/home/python/app -w /home/python/app dkshs/python_dev
```

## License

This project is under the [MIT](/LICENSE) license.
