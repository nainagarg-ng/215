#!/bin/bash

set -e

# Create the network if we don't have it yet
docker network inspect data-processor-network >/dev/null 2>&1 || docker network create data-processor-network

# Build the image based on the Dockerfile
docker build -t data-processor -f Dockerfile .

# Run All Containers
docker-compose run data-processor