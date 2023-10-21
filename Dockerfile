FROM python:3.11.6-slim-bullseye

ARG USERNAME=dev-user
ARG APP_HOME=/home/${USERNAME}/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt update && apt install --no-install-recommends -y \
  sudo git gpg gnupg gpg-agent socat ssh \
  zsh \
  curl \
  wget \
  fonts-powerline \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# Create user and add it to sudoers
RUN groupadd --gid 1000 ${USERNAME} \
  && useradd --uid 1000 --gid ${USERNAME} --shell /bin/zsh --create-home ${USERNAME} \
  && echo ${USERNAME} ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/${USERNAME} \
  && chmod 0440 /etc/sudoers.d/${USERNAME}

WORKDIR ${APP_HOME}

COPY ./.docker/start.sh /start.sh
RUN sed -i 's/\r$//g' /start.sh
RUN chmod +x /start.sh

RUN wget https://gist.github.com/dkshs/ab9fdbb2cc4b6af40ef3627d4ba968a4/raw/df2cf7829dd00549f8d7889254f5db017a10a8b8/.p10k.zsh && \
  mv ./.p10k.zsh /home/${USERNAME}

USER ${USERNAME}

RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.1.5/zsh-in-docker.sh)" -- \
  -p git \
  -p git-flow \
  -p ssh-agent \
  -p https://github.com/zdharma-continuum/fast-syntax-highlighting \
  -p https://github.com/zsh-users/zsh-autosuggestions \
  -p https://github.com/zsh-users/zsh-completions \
  -a "export TERM=xterm-256color"

RUN echo "[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh" >> ~/.zshrc && \
  echo "HISTFILE=~/.zsh_history" >> ~/.zshrc && \
  echo "export PATH=$HOME/.local/bin:/usr/local/bin:$PATH" >> ~/.zshrc && \
  echo "eval '$(ssh-agent -s)'" >> ~/.zshrc

CMD [ "/start.sh" ]