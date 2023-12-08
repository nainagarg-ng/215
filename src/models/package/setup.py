from setuptools import find_packages, setup

REQUIRED_PACKAGES = ["wandb==0.15.11", 
                     "torch==1.13.1",
                     "scikit-learn",
                     "dask",
                     "transformers",
                     "google-cloud-secret-manager",
                     "argparse"]

setup(
    name="dga-trainer",
    version="0.0.1",
    install_requires=REQUIRED_PACKAGES,
    packages=find_packages(),
    description="DGA App Trainer Application",
)