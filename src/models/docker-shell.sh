#env variables in ~/.bash_profile or can be set in ~/.bashrc
export BASE_DIR=$(pwd)

# Build the image based on the Dockerfile
#docker build -t $IMAGE_NAME -f Dockerfile .

# M1/2 chip macs use this line
docker build -t $IMAGE_NAME --platform=linux/arm64/v8 -f Dockerfile .

#docker build ./ -t $EXECUTOR_IMAGE_URI

# Run Container
docker run --rm --name $IMAGE_NAME -ti \
-v "$BASE_DIR":/app \
-v "$SECRETS_DIR_train":/secrets \
-e GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS_data \
-e GCP_PROJECT=$GCP_PROJECT \
-e GCS_BUCKET_URI=$GCS_BUCKET_URI \
-e GCP_REGION=$GCP_REGION \
-e WANDB_KEY=$WANDB_KEY \
$IMAGE_NAME

