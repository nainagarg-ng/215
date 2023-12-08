
#######################
###### IMPORTS ######
#######################

import os
import argparse
import random
import string
import json
import sys
from kfp import dsl
from kfp import compiler
import google.cloud.aiplatform as aip
from model2 import data_training

#######################
###### CONSTANTS ######
#######################

GCS_BUCKET_NAME = "dga-workflow"
BUCKET_URI = f"gs://{GCS_BUCKET_NAME}"
PIPELINE_ROOT = f"{BUCKET_URI}/pipeline_root/root"
GCS_SERVICE_ACCOUNT="model-trainer@harvardmlops.iam.gserviceaccount.com"
GCP_PROJECT="harvardmlops"
GCP_REGION = os.environ["GCP_REGION"]
GCS_BUCKET_URI = "gs://dga-training"
WANDB_KEY = os.environ["WANDB_KEY"]


# google application creds
creds = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', 0)
if creds:
    with open(creds, "r") as f:
        token = json.load(f)
    data_token = json.dumps(token)
else:
    raise Exception("Error: GOOGLE_APPLICATION_CREDENTIALS Not Found")


#######################
###### FUNCTIONS ######
#######################

def generate_uuid(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))

def main(args=None):
    print("CLI Arguments:", args)

    #######################
    ####### EXTRACT #######
    #######################
    if args.data_extractor:

        # Define a Container Component
        @dsl.container_component
        def data_extractor():
            return dsl.ContainerSpec(
                image='mrrootb0t/data-extractor:pipeline',
                command=[],
                args=["extract.py"]
            )

        # Define a Pipeline
        @dsl.pipeline
        def data_extractor_pipeline():
            data_extractor()

        # Build yaml file for pipeline
        compiler.Compiler().compile(
            data_extractor_pipeline, package_path="data_extractor.yaml"
        )

        # Submit job to Vertex AI
        aip.init(project=GCP_PROJECT, staging_bucket=BUCKET_URI)

        job_id = generate_uuid()
        DISPLAY_NAME = "dga-data-extractor-" + job_id
        job = aip.PipelineJob(
            display_name=DISPLAY_NAME,
            template_path="data_extractor.yaml",
            pipeline_root=PIPELINE_ROOT,
            enable_caching=False,
        )

        job.run(service_account=GCS_SERVICE_ACCOUNT)


    #######################
    ####### FORMAT #######
    #######################
    if args.data_formator:
        
        # Define a Container Component
        @dsl.container_component
        def data_formator():
            return dsl.ContainerSpec(
                image='mrrootb0t/data-formator:pipeline',
                command=[],
                args=['format.py'])

        # Define a Pipeline
        @dsl.pipeline
        def data_formator_pipeline():
            data_formator()

        # Build yaml file for pipeline
        compiler.Compiler().compile(
            data_formator_pipeline, package_path="data_formator.yaml"
        )

        # Submit job to Vertex AI
        aip.init(project=GCP_PROJECT, staging_bucket=BUCKET_URI)

        job_id = generate_uuid()
        DISPLAY_NAME = "dga-data-formator-" + job_id
        job = aip.PipelineJob(
            display_name=DISPLAY_NAME,
            template_path="data_formator.yaml",
            pipeline_root=PIPELINE_ROOT,
            enable_caching=False
        )

        job.run(service_account=GCS_SERVICE_ACCOUNT)


    #######################
    ####### #TRAIN ########
    #######################
    if args.data_trainer:
        
        # Define a Container Component
        #@dsl.container_component
        #def data_trainer(epochs=1, batch_size=64, frac=0.00001, lr=1e-5):
        #    return dsl.ContainerSpec(
        #        image='mrrootb0t/train-dga-detector:pipeline',
        #        command=[],
        #        args=[])

        # Define a Pipeline
        @dsl.pipeline
        def data_trainer_pipeline():
            data_training(WANDB_KEY=WANDB_KEY, 
                          data_token=data_token,
                          GCP_PROJECT="harvardmlops",
                          GCP_REGION="us-central1",
                          GCS_BUCKET_URI="gs://dga-training")

        # Build yaml file for pipeline
        compiler.Compiler().compile(
            data_trainer_pipeline, package_path="data_trainer.yaml"
        )

        # Submit job to Vertex AI
        aip.init(project=GCP_PROJECT, staging_bucket=BUCKET_URI)

        job_id = generate_uuid()
        DISPLAY_NAME = "dga-data-trainer-" + job_id
        job = aip.PipelineJob(
            display_name=DISPLAY_NAME,
            template_path="data_trainer.yaml",
            pipeline_root=PIPELINE_ROOT,
            enable_caching=False,
        )

        job.run(service_account=GCS_SERVICE_ACCOUNT)

    #######################
    ###### PIPELINE #######
    #######################
    if args.pipeline:

        # Define a Container Component
        @dsl.container_component
        def data_extractor():
            return dsl.ContainerSpec(
                image='mrrootb0t/data-extractor:pipeline',
                command=[],
                args=["extract.py"]
            )
        
        # Define a Container Component
        @dsl.container_component
        def data_formator():
            return dsl.ContainerSpec(
                image='mrrootb0t/data-formator:pipeline',
                command=[],
                args=['format.py'])
        
        # Define a Pipeline
        @dsl.pipeline
        def ml_pipeline():

            # Data Extractor
            data_collector_task = data_extractor().set_display_name("Data Extractor")

            # Data Processor
            data_processor_task = data_formator().set_display_name("Data Formator").after(data_collector_task)
            
            # Model Training
            model_training_task = (
                data_training(WANDB_KEY=WANDB_KEY, 
                          data_token=data_token,
                          GCP_PROJECT="harvardmlops",
                          GCP_REGION="us-central1",
                          GCS_BUCKET_URI="gs://dga-training")
                .set_display_name("Model Training")
                .after(data_processor_task)
            )

        # Build yaml file for pipeline
        compiler.Compiler().compile(ml_pipeline, package_path="pipeline.yaml")

        # Submit job to Vertex AI
        aip.init(project=GCP_PROJECT, staging_bucket=BUCKET_URI)

        job_id = generate_uuid()
        DISPLAY_NAME = "dga-app-pipeline-" + job_id
        job = aip.PipelineJob(
            display_name=DISPLAY_NAME,
            template_path="pipeline.yaml",
            pipeline_root=PIPELINE_ROOT,
            enable_caching=False,
        )

        job.run(service_account=GCS_SERVICE_ACCOUNT)




if __name__ == "__main__":

    # Generate the inputs arguments parser
    # if you type into the terminal 'python cli.py --help', it will provide the description
    parser = argparse.ArgumentParser(description="Workflow CLI")

    parser.add_argument(
        "-e",
        "--data_extractor",
        action="store_true",
        help="Run just the Data Extractor",
    )
    parser.add_argument(
        "-f",
        "--data_formator",
        action="store_true",
        help="Run just the Data Formator",
    )
    parser.add_argument(
        "-t",
        "--data_trainer",
        action="store_true",
        help="Run just Model Training",
    )
    parser.add_argument(
        "-p",
        "--pipeline",
        action="store_true",
        help="DGA App Pipeline",
    )

    args = parser.parse_args()

    main(args)