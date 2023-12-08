import argparse
import os
import subprocess
from datetime import datetime

from google.cloud import storage

#This script extract raw data from open-source and saves to GCP storage

def calculate_month_day():
    # Get the current date
    current_date = datetime.now()
    
    # Extract the month and day as integers
    month = current_date.month
    day = current_date.day - 1
    
    # Typecast the integers to strings
    month_str = str(month)
    day_str = str(day)
    
    # Combine month and day into a single string
    month_day = f"{month_str}/{day_str}"
    
    return month_day


def upload(mlops_bucket, folder, project):

    # Initiate Storage client
    storage_client = storage.Client(project=project)

    # Get reference to bucket
    bucket = storage_client.bucket(mlops_bucket)

    # Local Destination path to raw data saved locally
    path_to_raw = "/app/data/bronze/"

    destination_blob_names = [f"{path_to_raw}{file}" for file in os.listdir(path_to_raw)]

    #month and day of extraction
    month_day = calculate_month_day()

    #save each file to GCP bucket/folder
    for destination_blob in destination_blob_names:
        blob = bucket.blob(f"{folder}/{month_day}/{destination_blob.split('/')[-1]}")
        blob.upload_from_filename(destination_blob)



def extract(mlops_bucket, folder, project):
    
    print("* Starting extraction")
    start = datetime.now()
    
    #shell script path for extracting DGA and benign data
    extractor = '/app/extract.sh'

    # Use subprocess to run the shell script
    try:
        subprocess.run(['bash', extractor], check=True)
        end = datetime.now()
        print(f"  -- Shell script executed successfully. Time to retrieve data: {end-start}")
    except subprocess.CalledProcessError as e:
        print(f"  -- Error running the shell script: {e}")
    
    print(f"* Uploading data to GCP Bucket named {mlops_bucket}")
    start = datetime.now()

   #method for uploading DGA and benign data
    upload(mlops_bucket, folder, project)

    end = datetime.now()
    print(f"  -- Time taken for upload: {end-start}")


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Data Extractor CLI")
    
    parser.add_argument(
        "-f", 
        "--folder", 
        type=str, 
        default="bronze", 
        help="Folder Name to save the data"
    )

    parser.add_argument(
        "-b", 
        "--bucket", 
        type=str, 
        default="harvardmlops", 
        help="Bucket Name to save the data"
    )

    parser.add_argument(
        "-p", 
        "--project", 
        type=str, 
        default="harvardmlops", 
        help="GCP Project Name"
    )

    args = parser.parse_args()

    # PROJECT NAME
    project = os.getenv("GCP_PROJECT")
    # If project was passed as argument
    if args.project != "":
        project = args.project

    #BUCKET NAME
    mlops_bucket = os.getenv("GCP_BUCKET")
    # If bucket was passed as argument
    if args.bucket != "":
        mlops_bucket = args.bucket

    # FOLDER NAME
    folder = os.getenv("GCP_BUCKET_BRONZE_FOLDER")
    # If bucket was passed as argument
    if args.folder != "":
        folder = args.folder

    extract(mlops_bucket, folder, project)