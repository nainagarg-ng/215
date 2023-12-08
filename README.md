Project Organization
--------------------
```
        ├── LICENSE
        ├── README.md
        ├── dga-classifier-app-v1
        │   ├── LICENSE
        │   ├── images
        │   └── src
        │       ├── api-service
        │       │   ├── Dockerfile
        │       │   ├── Pipfile
        │       │   ├── Pipfile.lock
        │       │   ├── api
        │       │   │   ├── model.py
        │       │   │   ├── service.py
        │       │   │   ├── tracker.py
        │       │   │   └── vertexAImodel.py   <---- WE DECIDED TO USE VERTEX AI ENDPOINT FOR THIS MILESTONE
        │       │   ├── docker-entrypoint.sh
        │       │   ├── docker-shell.bat
        │       │   └── docker-shell.sh
        │       ├── deployment
        │       │   ├── Dockerfile
        │       │   ├── deploy-*.yml files
        │       │   ├── docker-entrypoint.sh
        │       │   ├── docker-shell.bat
        │       │   ├── docker-shell.sh
        │       │   ├── inventory.yml
        │       │   └── nginx-conf
        │       │       └── nginx
        │       │           └── nginx.conf
        │       ├── frontend-react
        │       │   ├── Dockerfile
        │       │   ├── Dockerfile.dev
        │       │   ├── conf.d
        │       │   │   └── default.conf
        │       │   ├── docker-shell.bat
        │       │   ├── docker-shell.sh
        │       │   ├── package.json
        │       │   ├── public
        │       │   │   ├── index.html
        │       │   │   └── manifest.json
        │       │   ├── src
        │       │   │   ├── app
        │       │   │   │   ├── App.css
        │       │   │   │   ├── App.js
        │       │   │   │   └── App.test.js
        │       │   │   ├── components
        │       │   │   ├── index.css
        │       │   │   ├── index.js
        │       │   │   ├── services
        │       └── frontend-simple
        │           ├── Dockerfile
        │           ├── docker-shell.bat
        │           ├── docker-shell.sh
        │           ├── index.html
        ├── images
        ├── notebooks
        │   ├── EDA_and_Model.ipynb
        │   ├── model.ipynb
        │   ├── model_CNN_LSTM.ipynb
        │   └── tree_bert_based_experiments.ipynb
        ├── persistent
        │   └── experiments
        ├── references
        │   └── Chin2018_Chapter_AMachineLearningFrameworkForSt.pdf
        ├── reports
        │   ├── images
        │   ├── milestone2.md
        │   └── milestone3.md
        │   ├── milestone4.md
        └── src
            ├── deploy_model
            │   ├── Dockerfile
            │   ├── docker-shell.sh
            │   ├── handler.py     <------ HANDLER FOR DEPLOYING PYTORCH MODEL TO VERTEX AI
            │   ├── predict.py
            │   └── stage.py
            ├── etl
            │   ├── extracts
            │   │   ├── Dockerfile
            │   │   ├── Pipfile
            │   │   ├── Pipfile.lock
            │   │   ├── README.md
            │   │   ├── docker-compose.yml
            │   │   ├── docker-entrypoint.sh
            │   │   ├── docker-shell.sh
            │   │   ├── extract.py
            │   │   ├── extract.sh
            │   │   └── images
            │   ├── format
            │   │   ├── Dockerfile
            │   │   ├── Pipfile
            │   │   ├── Pipfile.lock
            │   │   ├── README.md
            │   │   ├── docker-compose.yml
            │   │   ├── docker-entrypoint.sh
            │   │   ├── docker-shell.sh
            │   │   ├── format.py
            │   │   └── images
            │   └── preprocess
            │       ├── Dockerfile
            │       ├── Pipfile
            │       ├── Pipfile.lock
            │       ├── README.md
            │       ├── docker-compose.yml
            │       ├── docker.sh
            │       ├── features.py
            │       ├── images
            │       └── preprocess.py
            ├── models
            │   ├── Dockerfile
            │   ├── Pipfile
            │   ├── Pipfile.lock
            │   ├── cli.py
            │   ├── docker-entrypoint.sh
            │   ├── docker-shell.sh
            │   ├── package
            │   │   ├── PKG-INFO
            │   │   ├── setup.cfg
            │   │   ├── setup.py
            │   │   └── trainer
            │   │       ├── __init__.py
            │   │       └── task.py
            │   └── package-trainer.sh
            ├── optimizations
            │   └── Quantization.ipynb
            ├── streamlit
            │   ├── Dockerfile
            │   ├── Pipfile
            │   ├── Pipfile.lock
            │   ├── cli.py
            │   ├── docker-compose.yml
            │   └── docker.sh
            └── workflow
                ├── Dockerfile
                ├── Pipfile
                ├── Pipfile.lock
                ├── cli.py
                ├── data_extractor.yaml
                ├── data_formator.yaml
                ├── data_trainer.yaml
                ├── docker-entrypoint.sh
                ├── docker-shell.sh
                ├── model.py
                └── pipeline.yaml
```

# AC215 - Milestone5 - CyberSafe

**Team Members**
- Rob Chavez
- Naina Garg
- Qian Liu
- Daniel More Torres
- Sophia Yang (She/Her)
  
<br>

**Group Name**
- CyberSafe

<br>

**Project**
- In this project we aim to develop an application that can identify the actors associated with domains produced by domain generating algorithms.

<br>

### Milestone5
Our Milestone 5 emphasizes the final stages of our project, focusing on the development and deployment of the DGA classifier application that ties together the various components built in our previous milestones. We have designed an intuitive user interface and deployed it in GCP to ensure the functionality of the project for real-world usage. In this milestone, we designed the overall architecture of our application, including the user interface, functionality, and underlying code structure to ensure maintainability and efficiency. We developed robust APIs that facilitate communication between the front end and back end of the application using VERTEX AI's deployed model endpoint. In regard to our deployment strategy, we utilized Ansible to create, provision, and deploy our frontend and backend to GCP in an automated fashion.

1). **Application Design Document:** The user can find our detailed design document including solution and technical architectures outlining the DGA classifier application architecture, user interface, and code organization principles here:

[Link to the Design Document (Google Slides)](https://docs.google.com/presentation/d/18nRPqZH9mjtGM8iJtijlz_zeByMHuvDeHMsd_OUqRqU/edit?usp=sharing)

![Solution Architecture 1](images/solution_architecture1.png)

![Solution Architecture 2](images/solution_architecture2.png)

![Technical Architecture 1](images/technical_architecture1.png)

![Technical Architecture 2](images/technical_architecture2.png)

2). APIs & Frontend Implementation: Working code for the APIs and front-end interface, complete with documentation and testing to verify proper functionality, can be found in this repo, `Milestone5`. 

The basic structure for our dga classifier app contains three containers: <b>api-service</b>, <b>frontend-simple</b>, and <b>frontend-react</b>.

## APIs

### Run api-service

The <b>api-service</b> contains three .py files: 

- <b>service.py</b>: Implement API service with FastAPI

- <b>tracker.py</b>: Download the best model: Here we are using `bert_dga_classifier` for our model. The downloaded model will be stored in `/persistent/experiments` folder.

- <b>model.py</b>: Load the model and use it to predict <--- we faced problems using the model because of platform issues between our Apple M1 processors and the VMs
- 
- <b>vertexAImodel.py</b>: Leverages VERTEX AI's endpoint to make predictions <--- This is the solution we ended up using

There are two predict functions:

- `predict_manual_input`: Predict when the user enters a domain name manually

- `predict_from_file`: Predict when the user uploads a .txt file

```
cd /dga-classifier-app-v1/src/api-service
sh docker-shell.sh
uvicorn-server
```

Then go to `http://localhost:9000/`

It shows a message: "{"message":"Welcome to the API Service"}".

If you go to `http://localhost:9000/docs#/`, you can see all the api services implemented:

![api service 1](images/api-service1.png)

![api service 2](images/api-service2.png)

## Frontend Implementation

### Run frontend-simple

(Note: frontend-simple is only used as a prototype and will not be deployed.)

```
cd /dga-classifier-app-v1/src/frontend-simple
sh docker-shell.sh
http-server
```

Then go to `http://localhost:8080/`

You can test a domain name by entering it manually:

![frontend simple 1](images/frontend-simple1.png)

![frontend simple 2](images/frontend-simple2.png)

Or you can upload a .txt file and get the result in a .txt file in the following format:

```
[
  {
    "domain": "cnn.com",
    "result": "legit"
  },
  {
    "domain": "asdgoaio1239z0dvnkmk.com",
    "result": "zeus-newgoz"
  }
]
```

### Run frontend-react

```
cd /dga-classifier-app-v1/src/frontend-react
sh docker-shell.sh
yarn install
yarn start
```

Then go to `http://localhost:3000/`

You can test a domain name by entering it manually:

![frontend react 1](images/frontend-react1.png)

![frontend react 2](images/frontend-react2.png)

Or you can upload a .txt file:

![frontend react 3](images/frontend-react3.png)

Note: it will show an alert message if the user is trying to upload a file that is not .txt:

![frontend react 4](images/frontend-react4.png)

Again, the downloaded result will look like this:

```
[
  {
    "domain": "cnn.com",
    "result": "legit"
  },
  {
    "domain": "asdgoaio1239z0dvnkmk.com",
    "result": "zeus-newgoz"
  }
]
```
