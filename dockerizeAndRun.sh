#!/usr/bin/env bash

SERVICE=wednesdaybot

docker build -t $SERVICE:latest .

docker run --name="wednesdaybot" -d $SERVICE:latest