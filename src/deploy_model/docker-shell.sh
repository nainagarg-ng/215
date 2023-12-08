#!/bin/bash

set -e

# Build the image based on the Dockerfile
docker build -t dga-deployed -f Dockerfile .

# Run Container
docker run --rm -it -p 7080:7080 -p 7081:7081  --platform=linux/amd64 --name dga-deployed dga-deployed