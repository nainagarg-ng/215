#!/bin/bash

# set -e

export SECRETS_DIR=$(pwd)/../secrets/
export WORKFLOW_IMAGE_NAME="ml-workflow"
export WORKFLOW_BASE_DIR=$(pwd)
export WORKFLOW_GCS_BUCKET_NAME="dga-workflow"
export WORKFLOW_GOOGLE_APPLICATION_CREDENTIALS="../secrets/model-trainer.json"
export WORKFLOW_GCS_SERVICE_ACCOUNT="model-trainer@harvardmlops.iam.gserviceaccount.com"
export WORKFLOW_GCP_REGION="us-central1"
export WORKFLOW_GCS_PACKAGE_URI="gs://dga-training"
export WORKFLOW_GCP_REGION="us-central1"
export GCP_BUCKET="harvardmlops"
export GCP_BUCKET_BRONZE_FOLDER="bronze"

# Build the image based on the Dockerfile
#docker build -t $IMAGE_NAME -f Dockerfile .
docker build -t $WORKFLOW_IMAGE_NAME --platform=linux/amd64 -f Dockerfile .

# Run Container
docker run --rm --name $WORKFLOW_IMAGE_NAME -ti \
-v /var/run/docker.sock:/var/run/docker.sock \
-v "$SECRETS_DIR":/secrets \
-v "$WORKFLOW_BASE_DIR":/app \
-v "$WORKFLOW_BASE_DIR/../etl/extracts":/data-collector \
-v "$WORKFLOW_BASE_DIR/../etl/extracts":/data-formator \
-e GOOGLE_APPLICATION_CREDENTIALS=$WORKFLOW_GOOGLE_APPLICATION_CREDENTIALS \
-e GCP_PROJECT=$GCP_PROJECT \
-e GCS_BUCKET_NAME=$WORKFLOW_GCS_BUCKET_NAME \
-e GCS_SERVICE_ACCOUNT=$WORKFLOW_GCS_SERVICE_ACCOUNT \
-e GCP_REGION=$WORKFLOW_GCP_REGION \
-e GCS_PACKAGE_URI=$WORKFLOW_GCS_PACKAGE_URI \
-e GCP_BUCKET=$GCP_BUCKET \
-e GCP_BUCKET_BRONZE_FOLDER=$GCP_BUCKET_BRONZE_FOLDER \
-e WANDB_KEY=$WANDB_KEY \
-e GCS_BUCKET_URI=$GCS_BUCKET_URI \
$WORKFLOW_IMAGE_NAME