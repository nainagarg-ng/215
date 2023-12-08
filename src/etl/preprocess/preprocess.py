import concurrent.futures
import os
from datetime import datetime

import gcsfs
import pandas as pd
import pyarrow
import pyarrow.parquet as pq
from features import *
from google.cloud import storage

project = os.environ["GCP_PROJECT"]
bucket_name = os.environ["GCP_BUCKET"]
bronze_folder = os.environ["GCP_BUCKET_BRONZE_FOLDER"]
silver_folder = os.environ["GCP_BUCKET_SILVER_FOLDER"]
gold_folder = os.environ["GCP_BUCKET_GOLD_FOLDER"]
token = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]

def calculate_month_day():
    # Get the current date
    current_date = datetime.now()

    # Typecast month integers to strings
    month_str = str(current_date.month)

    # Typecast day integers to strings
    day_str = str(current_date.day)
    
    # Combine month and day into a single string
    month_day = f"{month_str}/{day_str}"
    
    return month_day

month_day = calculate_month_day()


def upload(df, filename):

    dest = f"gs://{bucket_name}/{gold_folder}/{month_day}/{filename}" 

    try:
        # Create a GCSFS client
        gcs_client = gcsfs.GCSFileSystem(project='harvardmlops')

        # Convert the Pandas DataFrame to an Arrow Table
        table = pyarrow.Table.from_pandas(df)

        with gcs_client.open(dest, 'wb') as f:
            pq.write_table(table, f)

        #free memory
        del df

        return True
    
    except:

        #free memory
        del df

        return False

def preprocess(path):

    filename = path.split("/")[-1]

    try:
        df = pd.read_parquet(path, engine='pyarrow')
        
        functions = [length, entropy, number_of_vowels,
                    number_of_consonants, number_of_numbers, number_of_specials]
        
        for func in functions:
            df[func.__name__] = df['domains'].apply(func)

        if upload(df, filename):
            return True
        else:
            return False

    except:
        return False

def feature_engineer(tasks):

    print(f" * Starting Feature Engineering")
    
    #begin time
    start = datetime.now()

    #feature engineer data
    with concurrent.futures.ProcessPoolExecutor(max_workers=6) as executor:
        for response in executor.map(preprocess, tasks):
            if not response:
                raise Exception("Error: Feature Engineering Process Failed")

    #stop timing
    end = datetime.now()

    #give time result
    print(f"  -- Finished feature engineering of data in: {end-start}")
    print(f"  -- Data successfully saved to GCP Bucket")


def list_files(dir_path):

    #list files in fir_path
    files = os.listdir(dir_path)

    # List all file names in the "silver" folder
    file_paths = [os.path.join(dir_path, file) for file in files \
                    if os.path.isfile(os.path.join(dir_path, file))]
    
    return file_paths

def download():
    
    #msg & start timer
    print(f" * Starting download")

    start = datetime.now()

    # Initiate Storage client
    storage_client = storage.Client(project=project)

    # Get reference to bucket
    bucket = storage_client.bucket(bucket_name)

    # Find all content in a bucket
    blobs = bucket.list_blobs(prefix=silver_folder)

    #make dir path
    dir_path = f"{silver_folder}/{month_day}"

    # make dir if not already exists
    os.makedirs(dir_path, exist_ok=True)

    for blob in blobs:
        if not blob.name.endswith("/"):
            blob.download_to_filename(blob.name)

    end = datetime.now()

    print(f"  -- Download complete. Time Taken: {end-start}")

    return dir_path

def main():

    #download files into local dir & return local dir location
    download_path = download()
    print(download_path)

    #get list of files to feature engineer
    files = list_files(download_path)
    
    #feature engineer data in each file returned as list of dataframes
    feature_engineer(files)

if __name__ == "__main__":
    main()