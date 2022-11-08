#!/bin/zsh
# Docker image: https://hub.docker.com/r/dkshs/python_dev/
# Author: DKSHS
# Description: Container execution script

# Loading colors
autoload -U colors
colors

# echo "\033[0;32mContainer started\033 \n"
echo "$bold_color$fg[green]Container started \n${reset_color}"

# Showing Python and pip version
# echo "\033[0;32mPython version: $PYTHON_VERSION\033"
# echo "\033[0;32mPip version: $PYTHON_PIP_VERSION\033 \n"
echo "$bold_color$fg[blue]Python version: $PYTHON_VERSION"
echo "$bold_color$fg[blue]Pip version: $PYTHON_PIP_VERSION \n${reset_color}"

# Tip on how to enter the container via CLI
# echo "\033[0;32mRun this to enter the container via CLI:\033[0m"
echo "$bold_color$fg[cyan]Run this to enter the container via CLI:${reset_color}"
echo "$ docker exec -it $HOSTNAME zsh \n"

# echo "\033[0;32mContainer is running\033[0m"
echo "$bold_color$fg[green]Container is running...${reset_color}"
# locking the container
tail -f /dev/null
