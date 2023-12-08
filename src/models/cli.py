import os
import json
import random
import string
import google.cloud.aiplatform as aip

GCP_PROJECT = os.environ["GCP_PROJECT"]
GCP_REGION = os.environ["GCP_REGION"]
GCS_BUCKET_URI = os.environ["GCS_BUCKET_URI"]
WANDB_KEY = os.environ["WANDB_KEY"]

# google application creds
creds = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', 0)
if creds:
    with open(creds, "r") as f:
        token = json.load(f)
    data_token = json.dumps(token)
else:
    raise Exception("Error: GOOGLE_APPLICATION_CREDENTIALS Not Found")

#ENV VARIABLES
environment_variables = {"data_token":data_token,
                         "wandb_key": WANDB_KEY}

def generate_uuid(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))


# Initialize Vertex AI SDK for Python
aip.init(project=GCP_PROJECT, location=GCP_REGION, staging_bucket=GCS_BUCKET_URI)

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

CMDARGS = ["--epochs=1", "--batch_size=64", "--frac=0.00001"]
MODEL_DIR = GCS_BUCKET_URI
TRAIN_COMPUTE = "n1-standard-4"
TRAIN_GPU = "NVIDIA_TESLA_T4"
TRAIN_NGPU = 1

print(f"{GCS_BUCKET_URI}/trainer.tar.gz")
print(TRAIN_IMAGE)

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