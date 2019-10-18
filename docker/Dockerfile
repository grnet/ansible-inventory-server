FROM ubuntu:18.04
MAINTAINER Stamatis Katsaounis "skatsaounis@admin.grnet.gr"

ARG BRANCH=master

RUN apt update && \
    apt install -y \
        python3-pip \
        python3-setuptools \
        software-properties-common \
        curl \
        git \
        --no-install-recommends && \
    add-apt-repository -yu ppa:juju/stable && \
    apt update && \
    apt install -y \
        juju \
        --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

RUN git init /src/ansible-inventory-server && \
    (cd /src/ansible-inventory-server && \
        git fetch --tags https://github.com/grnet/ansible-inventory-server.git $BRANCH && \
        git checkout FETCH_HEAD) && \
    pip3 install --no-cache-dir /src/ansible-inventory-server && \
    rm -r /src/ansible-inventory-server && \
    mkdir -p /usr/local/lib/python3.6/site-packages/ansible_inventory_server/config
