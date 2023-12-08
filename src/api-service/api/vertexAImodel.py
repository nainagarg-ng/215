from typing import Dict, List, Union

from google.cloud import aiplatform
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value


def predict_custom_trained_model_sample(
    project: str,
    endpoint_id: str,
    instances: Union[Dict, List[Dict]],
    location: str = "us-central1",
    api_endpoint: str = "us-central1-aiplatform.googleapis.com",
):
    """
    `instances` can be either single instance of type dict or a list
    of instances.
    """
    # The AI Platform services require regional API endpoints.
    client_options = {"api_endpoint": api_endpoint}
    # Initialize client that will be used to create and send requests.
    # This client only needs to be created once, and can be reused for multiple requests.
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)
    # The format of each instance should conform to the deployed model's prediction input schema.
    instances = instances if isinstance(instances, list) else [instances]
    instances = [
        json_format.ParseDict(instance_dict, Value()) for instance_dict in instances
    ]
    parameters_dict = {}
    parameters = json_format.ParseDict(parameters_dict, Value())
    endpoint = client.endpoint_path(
        project=project, location=location, endpoint=endpoint_id
    )
    response = client.predict(
        endpoint=endpoint, instances=instances, parameters=parameters
    )
    print("response")
    print(" deployed_model_id:", response.deployed_model_id)
    # The predictions are a google.protobuf.Value representation of the model's predictions.
    predictions = response.predictions
    results = []
    for prediction in predictions:
        print(" prediction:", dict(prediction))
        results.append(dict(prediction))

    return results


def predict_manual_input(input):
    results = predict_custom_trained_model_sample(
        project="222163854742",  # 222163854742
        endpoint_id="3745431384437555200",  # 3745431384437555200
        location="us-central1",
        instances=[{"domain": input}],
    )
    print(results)
    response = []
    for result in results:
        for k, v in result.items():
            response.append({"domain": k, "result": v})

    return response[0]


def predict_file_from_path(file_path):
    # Check file extension
    if file_path.endswith(".txt"):
        with open(file_path, "r") as file:
            # Read file and split by newlines
            domains = file.read().splitlines()
            # Process the data as per requirement
            instances = [{"domain": domain.strip()} for domain in domains]

        results = predict_custom_trained_model_sample(
            project="222163854742",
            endpoint_id="3745431384437555200",
            location="us-central1",
            instances=instances,
        )
        print(results)
        response = []
        for result in results:
            for k, v in result.items():
                response.append({"domain": k, "result": v})
        return results

    else:
        raise ValueError("Unsupported file format. Please provide a .txt file.")
