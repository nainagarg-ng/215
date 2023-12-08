import asyncio
import os
from tempfile import TemporaryDirectory

import pandas as pd
from api import vertexAImodel
from api.tracker import TrackerService
from fastapi import Body, FastAPI, File
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

# Initialize Tracker Service
tracker_service = TrackerService()

# Setup FastAPI app
app = FastAPI(title="API Server", description="API Server", version="v2")

# Enable CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=False,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class InputData(BaseModel):
    name: str


@app.on_event("startup")
async def startup():
    print("Startup tasks")
    # Start the tracker service
    asyncio.create_task(tracker_service.track())


# Routes
@app.get("/")
async def get_index():
    return {"message": "Welcome to the API Service - Vertex AI"}


@app.post("/predict_manual_input")
async def predict1(input_data: InputData):
    # Make prediction
    prediction_results = vertexAImodel.predict_manual_input(input_data.name)
    return prediction_results


@app.post("/predict_from_file")
async def predict2(file: bytes = File(...)):
    # Save the file
    with TemporaryDirectory() as file_dir:
        file_path = os.path.join(file_dir, "test.txt")
        with open(file_path, "wb") as output:
            output.write(file)

        # Make Prediction
        prediction_results = vertexAImodel.predict_file_from_path(file_path)
        print(prediction_results)
        return prediction_results
