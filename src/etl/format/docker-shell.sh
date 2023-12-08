#!/bin/bash

set -e

# Create the network if we don't have it yet
docker network inspect data-formator-network >/dev/null 2>&1 || docker network create data-formator-network

# Build the image based on the Dockerfile
docker build -t data-formator --platform=linux/amd64/v2 -f Dockerfile .

# Run All Containers
docker-compose run data-formator