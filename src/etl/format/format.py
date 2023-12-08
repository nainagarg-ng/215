import argparse
import os
import sys
from datetime import datetime

import fastparquet
import pandas as pd
from google.cloud import storage

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


def download(project, bucket_name, bronze_folder):

    # Initiate Storage client
    storage_client = storage.Client(project=project)

    # Get reference to bucket
    bucket = storage_client.bucket(bucket_name)

    # Find all content in a bucket
    blobs = bucket.list_blobs(prefix=f"{bronze_folder}")

    month_day = calculate_month_day()

    # make local file
    os.makedirs(f"{bronze_folder}/{month_day}", exist_ok=True)

    for blob in blobs:
        blob_piece = (blob.name).split("/")
        date_piece = month_day.split("/")
        if len(blob_piece) <= 2:
            pass
        else:
            month = blob_piece[1]
            day = blob_piece[2]

            if (date_piece[0] == blob_piece[1]) and (date_piece[1] == blob_piece[2]):
                if not blob.name.endswith("/"):
                    blob.download_to_filename(blob.name)
    

def chunk_and_save(df, silver_folder):

    # Determine the size of the original DataFrame in megabytes
    original_size_mb = df.memory_usage(deep=True).sum() / (1024 * 1024)
    
    # Calculate the number of chunks required to fit within 100 megabytes each
    chunk_size_mb = 100
    num_chunks = int(original_size_mb / chunk_size_mb) + 1
    
    # Create directory
    month_day = calculate_month_day()
    dest_dir = f"{silver_folder}/{month_day}"
    os.makedirs(dest_dir, exist_ok=True)
    
    # Split the DataFrame into chunks and save each chunk
    for i in range(num_chunks):
        start_idx = i * int(len(df) / num_chunks)
        end_idx = (i + 1) * int(len(df) / num_chunks)
        chunk_df = df.iloc[start_idx:end_idx]
        
        # Save the chunked DataFrame to the "silver" folder
        chunk_df.to_parquet(f"{dest_dir}/chunk_{i}.gzip", 
                               compression='gzip',
                               index=False)

def format(bronze_folder, silver_folder):

    #path to raw data
    month_day = calculate_month_day()
    path = f"{bronze_folder}/{month_day}/"

    #the text files in the raw data are (1) named after the hacker group and (2) all end in list.txt
    cut_length = len("list.txt") + 1

    #list all the files in the path
    files = os.listdir(path)

    #create a dataframe that will hold all my data
    dga_df = pd.DataFrame()

    #loop through each file
    for file in files:
        
        #if it ends with .txt, it was pulled from https://data.mendeley.com/datasets/y8ph45msv8/1
        if file.endswith(".txt"):

            #the files contain a domain per line. Go through each line and append to domains list
            with open(f"{path}/{file}") as f:
                domains = []
                line = f.readline()
                while line != "":
                    line = f.readline()
                    if line != "":
                        domains.append(line.strip("\n"))
            
            #convert domains list into dataframe and add features isdga and actor                    
            df = pd.DataFrame(domains, columns=["domains"])
            df['actor'] = file[:-cut_length]

            #concat to final df
            dga_df = pd.concat([dga_df, df], axis=0)
            
        #else it was pulled from https://majestic.com/reports/majestic-million
        elif file.endswith(".csv"):
            #read csv into pandas DF, add features isdga and actor, drop others, concat to dga_df
            df = pd.read_csv(f"{path}/{file}", index_col=0, usecols=["Domain"])
            df['actor'] = "not_dga"
            dga_df = pd.concat([dga_df, df], axis=0)

    #shuffle dataframe
    dga_df = dga_df.sample(frac=1, random_state=42)
    dga_df.reset_index(inplace=True)
    dga_df.drop('index', inplace=True, axis=1)

    chunk_and_save(dga_df, silver_folder)


def upload(project, bucket_name, silver_folder):

    # Initiate Storage client
    storage_client = storage.Client(project=project)

    # Get reference to bucket
    bucket = storage_client.bucket(bucket_name)

    # Destination path in GCS 
    month_day = calculate_month_day()
    dest_dir = f"{silver_folder}/{month_day}"
    blob_files = os.listdir(dest_dir)
    destination_blob_names = [f"{dest_dir}/{blob_file}" \
                                for blob_file in blob_files]
    
    for destination_blob in destination_blob_names:
        blob = bucket.blob(destination_blob)
        blob.upload_from_filename(destination_blob)


def main():

    parser = argparse.ArgumentParser(description="Data Extractor CLI")
    
    parser.add_argument(
        "-f", 
        "--folder", 
        type=str, 
        default="bronze", 
        help="Folder Name to pull the data"
    )
    parser.add_argument(
        "-s", 
        "--silver_folder", 
        type=str, 
        default="silver", 
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

    # Bronze FOLDER NAME
    folder = os.getenv("GCP_BUCKET_BRONZE_FOLDER")
    # If bucket was passed as argument
    if args.folder != "":
        folder = args.folder

    # Silver FOLDER NAME
    silver = os.getenv("GCP_BUCKET_SILVER_FOLDER")
    # If bucket was passed as argument
    if args.silver_folder != "":
        silver = args.silver_folder


    print(f" * Pulling raw data from folder {folder} in GCP bucket {mlops_bucket}")
    start = datetime.now()
    download(project, mlops_bucket, folder)
    end = datetime.now()
    print(f"  -- Data pull complete. Time taken: {end-start}")


    print(f" * Parsing and Formatting Data")
    start = datetime.now()
    format(folder, silver)
    end = datetime.now()
    print(f"  -- Parsing/Formatting Complete. Time taken: {end-start}")


    print(f" * Saving parsed/formatted data to folder {silver} in GCP bucket {mlops_bucket}")
    start = datetime.now()       
    upload(project, mlops_bucket, silver)
    end = datetime.now()
    print(f"  -- Save complete. Time taken: {end-start}")


if __name__ == "__main__":

    main()