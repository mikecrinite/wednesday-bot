#!/usr/bin/env bash

SERVICE=wednesdaybot

# Stop any running wb
docker stop wednesdaybot
docker rm wednesdaybot

docker build -t $SERVICE .
docker run --name=$SERVICE -d --restart on-failure $SERVICE
