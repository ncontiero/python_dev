FROM python:3.8.10-slim

RUN apt update && apt install --no-install-recommends -y \
  git gpg gnupg gpg-agent socat \
  zsh \
  curl \
  wget \
  fonts-powerline

RUN useradd -ms /bin/bash python
USER python

WORKDIR /home/python/app

RUN wget https://gist.github.com/ShadowsS01/ab9fdbb2cc4b6af40ef3627d4ba968a4/raw/df2cf7829dd00549f8d7889254f5db017a10a8b8/.p10k.zsh && \
  mv ./.p10k.zsh ../

RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.1.3/zsh-in-docker.sh)" -- \
  -t https://github.com/romkatv/powerlevel10k \
  -p git \
  -p git-flow \
  -p https://github.com/zdharma-continuum/fast-syntax-highlighting \
  -p https://github.com/zsh-users/zsh-autosuggestions \
  -p https://github.com/zsh-users/zsh-completions \
  -a "export TERM=xterm-256color"

RUN echo "[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh" >> ~/.zshrc && \
  echo "HISTFILE=/home/python/zsh/.zsh_history" >> ~/.zshrc && \
  echo "export PATH=$HOME/.local/bin:/usr/local/bin:$PATH" >> ~/.zshrc

RUN wget https://gist.github.com/ShadowsS01/d55136902ab2e38527afa986f7d3eb1b/raw/0417ffd9077d86ac0d29195f9fa15d8bd8ce7eac/.startContainer.sh && \
  chmod +x ./.startContainer.sh && \
  mv ./.startContainer.sh ..

EXPOSE 8080

CMD [ "../.startContainer.sh" ]