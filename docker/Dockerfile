FROM python:3.6-slim-buster

ARG VERSION=1.1.2

COPY ansible_inventory_server /app/ansible_inventory_server/
COPY setup.cfg setup.py requirements.txt README.md /app/

ENV PBR_VERSION=$VERSION

RUN pip3 install --no-cache-dir /app
