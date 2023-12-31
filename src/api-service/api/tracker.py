import os
import traceback
import asyncio
from glob import glob
import json
import pandas as pd

#import tensorflow as tf
from google.cloud import storage


bucket_name = os.environ["GCS_BUCKET_NAME"]
local_experiments_path = "/persistent/experiments"

# Setup experiments folder
if not os.path.exists(local_experiments_path):
    os.mkdir(local_experiments_path)


def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

def download_best_model():
    print("Download best model")
    try:
        best_model = {'experiment': 0, 'model_name': "bert_dga_classifier"}
        # Create a json file best_model.json
        with open(
            os.path.join(local_experiments_path, "best_model.json"), "w"
        ) as json_file:
            json_file.write(json.dumps(best_model))

        # Download model
        download_file = os.path.join(
            best_model["model_name"] + ".pt"
        )
        download_blob(
            bucket_name,
            download_file,
            os.path.join(local_experiments_path, download_file),
        )

    except:
        print("Error in download_best_model")
        traceback.print_exc()


class TrackerService:
    def __init__(self):
        self.timestamp = 0

    async def track(self):
        # Download best model
        if os.path.exists("/persistent/experiments/bert_dga_classifier.pt"):
            print(f"Best model downloaded")
        else:
            download_best_model()


                
                
