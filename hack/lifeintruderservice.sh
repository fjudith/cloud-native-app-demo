#!/bin/bash
docker-compose \
--file ./src/lifeintruderservice/docker-compose.yaml \
build && \
docker-compose \
--file ./src/lifeintruderservice/docker-compose.yaml \
up