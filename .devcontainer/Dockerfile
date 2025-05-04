FROM ubuntu:noble

ENV DEBIAN_FRONTEND=noninteractive

RUN --mount=type=cache,target=/var/cache/apt --mount=type=cache,target=/var/lib/apt \ 
    apt-get update && apt-get install -y --no-install-recommends \
    g++ \
    gcc \
    tzdata \
    curl \
    wget \
    zip \
    jq \
    git \
    vim \
    make \
    software-properties-common \
    python3-pip \
    bash-completion \
    build-essential \
    unzip \ 
    less \ 
    && apt-get upgrade -y


RUN echo 'git config --global credential.helper "cache --timeout=99999"' >> ~/.bashrc

RUN cat <<EOF >> ~/.bashrc
parse_git_branch() {
    git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/(\\1)/'
}
PS1='\$(code=\${?##0};echo \${code:+\[\e[91m\][\${code}]})\[\e[0m\]\u@\h \[\e[32m\]\w \[\e[91m\]\$(parse_git_branch)\[\e[m\]λ '
EOF


# install docker, can comment this out if you don't want to control docker from the container
RUN --mount=type=cache,target=/var/cache/apt --mount=type=cache,target=/var/lib/apt \ 
    install -m 0755 -d /etc/apt/keyrings \
    && curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg \
    && chmod a+r /etc/apt/keyrings/docker.gpg \
    && echo \
        "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
        "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
        tee /etc/apt/sources.list.d/docker.list > /dev/null \
    && apt-get update \ 
    && apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# install awscli
RUN --mount=type=cache,target=/var/cache/apt --mount=type=cache,target=/var/lib/apt \ 
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install \
    && rm -rf awscliv2.zip aws



