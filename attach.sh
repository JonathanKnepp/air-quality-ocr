#!/bin/bash

CONTAINER_NAME="air-quality-ocr-app"

CONTAINER_ID=`docker container ps | grep "$CONTAINER_NAME" | awk '{print $1}'`
sudo docker exec -i -t ${CONTAINER_ID} /bin/bash
