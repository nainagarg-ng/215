#!/bin/bash

set -e

# Create the network if we don't have it yet
docker network inspect streamlit-app-network >/dev/null 2>&1 || docker network create streamlit-app-network

# Build the image based on the Dockerfile
docker build -t streamlit-app -f Dockerfile .

# Run All Containers
docker-compose run -p 8501:8501 streamlit-app