#!/bin/bash
echo "Rebuilding containers with docker-compose"
docker compose build

echo "Starting containers with docker-compose"
docker compose up --remove-orphans
