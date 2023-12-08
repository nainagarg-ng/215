

from kfp import dsl


# Define a Container Component
@dsl.component(base_image="python:3.10", packages_to_install=["google-cloud-aiplatform"])
def data_training(
    WANDB_KEY: str,
    data_token: str,
    GCP_PROJECT: str,
    GCP_REGION: str,
    GCS_BUCKET_URI: str,
    epochs: int = 1,
    lr: float = 1e-5,
    batch_size: int = 64,
    frac: float =0.0001,
    model_name: str = "bert-base-uncased",
):
    print("Model Training Job")

    import os
    import json
    import random
    import string
    import google.cloud.aiplatform as aip

    #ENV VARIABLES
    environment_variables = {"data_token":data_token,
                            "wandb_key": WANDB_KEY}

    # Initialize Vertex AI SDK for Python
    aip.init(project=GCP_PROJECT, location=GCP_REGION, staging_bucket=GCS_BUCKET_URI)

    def generate_uuid(length: int = 8) -> str:
        return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))

    job_id = generate_uuid()
    DISPLAY_NAME = "dga_classifier_test" + job_id

    TRAIN_IMAGE = "us-docker.pkg.dev/vertex-ai/training/pytorch-gpu.1-13.py310:latest"

    job = aip.CustomPythonPackageTrainingJob(
        display_name=DISPLAY_NAME,
        python_package_gcs_uri=f"{GCS_BUCKET_URI}/trainer.tar.gz",
        python_module_name="trainer.task",
        container_uri=TRAIN_IMAGE,
        project=GCP_PROJECT
    )

    CMDARGS = [f"--epochs={epochs}", 
               f"--batch_size={batch_size}", 
               f"--frac={frac}",
               f"--lr={lr}",
               f"--model_name={model_name}"]
    
    MODEL_DIR = GCS_BUCKET_URI
    TRAIN_COMPUTE = "n1-standard-4"
    #TRAIN_GPU = "NVIDIA_TESLA_T4"
    #TRAIN_NGPU = 1

    print(f"{GCS_BUCKET_URI}/trainer.tar.gz")
    #print(TRAIN_IMAGE)

    # Run the training job on Vertex AI
    # sync=True, # If you want to wait for the job to finish
    try:
        job.run(
            model_display_name=None,
            args=CMDARGS,
            replica_count=1,
            machine_type=TRAIN_COMPUTE,
            #accelerator_type=TRAIN_GPU,
            #accelerator_count=TRAIN_NGPU,
            base_output_dir=MODEL_DIR,
            environment_variables=environment_variables,
            sync=True,
        )
    except Exception as err:
        print(err)