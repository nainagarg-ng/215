#!/usr/bin/env python
# coding: utf-8

import argparse
import json
import os
import random
import string
import sys
from datetime import datetime

import numpy as np
#TORCH
import torch
#WANDB
import wandb
from torch.utils.data import DataLoader, TensorDataset

seed = 42
random.seed(seed)
np.random.seed(seed)
torch.manual_seed(seed)
torch.cuda.manual_seed_all(seed)

#DASK
import dask.dataframe as dd
#GOOGLE.CLOUD
from google.cloud import secretmanager
#SKLEARN
from sklearn.model_selection import train_test_split
#TRANSFORMERS
from transformers import (AdamW, AutoModel, AutoTokenizer,
                          BertForSequenceClassification, BertTokenizer,
                          DebertaForSequenceClassification,
                          DistilBertForSequenceClassification,
                          DistilBertTokenizer)

############################
######## CONSTANTS #########
############################

# key value of my secret
secrets = { "project_secret": "harvardmlops_json",
            "trainer_secret": "new_trainer_json"}

#name of the GCP project
project_id = 'harvardmlops'

#name of GCP data bucket
bucket_name = "harvardmlops"

#name of dga training bucket to save models and trainer.tar.gz
train_bucket = "dga-trainer"

#name of bucket folder to read
gold_folder = "gold"

#bucket_token
bucket_token = os.environ.get('data_token', 0)

#location of GCP bucket/folder files
files = f"gs://{bucket_name}/{gold_folder}/*/*/*.gzip"

#bucket to save models
save_path = f"/gcs/{train_bucket}/models/"

#labels of the DGA actors
actors = {'symmi':0, 'legit':1, 'ranbyus_v1':2, 'kraken_v1':3, 'not_dga':4, 'pushdo':5,
          'ranbyus_v2':6, 'zeus-newgoz':7, 'locky':8, 'corebot':9, 'dyre':10, 'shiotob':11,
          'proslikefan':12, 'nymaim':13, 'ramdo':14, 'necurs':15, 'tinba':16, 'vawtrak_v1':17,
          'qadars':18, 'matsnu':19, 'fobber_v2':20, 'alureon':21, 'bedep':22, 'dircrypt':23,
          'rovnix':24, 'sisron':25, 'cryptolocker':26, 'fobber_v1':27, 'chinad':28,
          'padcrypt':29, 'simda':30}

#device cpu/gpu option
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


############################
######### FUNCTIONS ########
############################

def generate_uuid(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))


def get_args():

    # Setup the arguments for the trainer task
    parser = argparse.ArgumentParser()

    parser.add_argument("--lr",
                        dest="lr",
                        default=1e-5,
                        type=float,
                        help="Learning rate.")

    parser.add_argument("--model_name",
                        dest="model_name",
                        default="bert-base-uncased",
                        type=str,
                        help="Model name")

    parser.add_argument("--epochs",
                        dest="epochs",
                        default=3,
                        type=int,
                        help="Number of epochs.")

    parser.add_argument("--batch_size",
                        dest="batch_size",
                        default=64,
                        type=int,
                        help="Size of a batch.")
    
    parser.add_argument("--frac",
                        dest="frac",
                        default=0.001,
                        type=float,
                        help="Random sample fraction to test data on")

    parser.add_argument("--wandb_key",
                        dest="wandb_key",
                        default=f"{os.environ.get('wandb_key', 0)}",
                        type=str,
                        help="WandB API Key")

    args = parser.parse_args()

    return args

def get_token(type):

    # Create a local secrets manager client:
    client = secretmanager.SecretManagerServiceClient()

    # get the secret name
    secret_name = secrets.get(type)

    # resource F string
    resource_name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"

    # ask the client to get my secret
    response = client.access_secret_version(request={"name": resource_name})

    # decode the response
    secret_string = response.payload.data.decode('UTF-8')

    # token access
    token = json.loads(secret_string)

    return token


def read(files:str, token):

    #storage option paramenter
    storage_options={'token': json.loads(token)}

    #begin time
    start = datetime.now()

    #read files as parquest
    df = dd.read_parquet(files, storage_options=storage_options)

    #stop timing
    end = datetime.now()

    #give time result
    print(f"Read data from in GCP bucket in: {end-start}")

    #ensure domain is str
    df['domains'] = df['domains'].astype(str)

    return df


def get_data(token, frac=0.0001, random_state=42):

    #get trainer_secret token from secrets manager
    token = bucket_token if (bucket_token) else get_token("trainer_secret") 

    #read files into a dask dataframe
    df = read(files, token)

    #convert to pandas DF for first transformation
    pandas_df = df.compute()

    #sample dataframe
    sampled_df = pandas_df.sample(frac=frac, random_state=random_state)

    return sampled_df


def tokenize_data(model_name, data):

    # init tokenizer
    if model_name == 'bert-base-uncased':
        tokenizer = BertTokenizer.from_pretrained(model_name)

    elif model_name == 'distilbert-base-uncased':
        tokenizer = DistilBertTokenizer.from_pretrained(model_name)

    elif model_name == 'microsoft/deberta-base':
        tokenizer = AutoTokenizer.from_pretrained(model_name)

    else:
        raise Exception("Model not found")
        sys.exit(1)

    # tokenize the data/domains
    tokenized_text = [tokenizer.encode(domain, truncation=True, add_special_tokens=True, max_length=20, pad_to_max_length=True) for domain in data['domains']]

    # map str labels to int
    labels = data['actor'].map(actors)

    return  tokenized_text, labels


def split_data(tokenized_text, labels, batch_size, random_state=42):

    # Split the data to get test data - 20 percent
    X_train, X_test, y_train, y_test = train_test_split(tokenized_text, labels, test_size=0.2, random_state=random_state)

    # Split again to get train and validation data
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.1, random_state=random_state)

    #X_train and y_train LongTensor
    X_train, y_train = torch.LongTensor(X_train), torch.LongTensor(np.array(y_train))

    #X_val and y_val LongTensor
    X_val, y_val = torch.LongTensor(X_val),torch.LongTensor(np.array(y_val))

    #X_test and y_test LongTensor
    X_test, y_test = torch.LongTensor(X_test), torch.LongTensor(np.array(y_test))

    #training dataloader
    train_loader = DataLoader(TensorDataset(X_train, y_train), batch_size=batch_size, shuffle=True)

    #validation dataloader
    val_loader = DataLoader(TensorDataset(X_val, y_val), batch_size=batch_size, shuffle=False)

    #test dataloader
    test_loader = DataLoader(TensorDataset(X_test, y_test), batch_size=batch_size, shuffle=False)

    return train_loader, val_loader, test_loader


def get_model(model_name, data, lr):

    num_labels = len(data['actor'].unique())

    #MODEL 1
    if model_name == 'bert-base-uncased':
        model = BertForSequenceClassification.from_pretrained(model_name, num_labels=num_labels)

    #MODEL 2
    elif model_name == 'distilbert-base-uncased':
        model = DistilBertForSequenceClassification.from_pretrained(model_name, num_labels=num_labels)

    #MODEL 3
    elif model_name == 'microsoft/deberta-base':
        model = DebertaForSequenceClassification.from_pretrained(model_name, num_labels=num_labels)

    else:
        raise Exception("Model Not Found")
        sys.exit(0)

    model = model.to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr)

    return model, optimizer


############################
######### PROCESS ##########
############################

# COLLECT ARGS
args = get_args()

# RETRIEVE DATA
data = get_data(bucket_token, frac=args.frac)
#data = get_data(bucket_token, frac=0.001)

# GET MODEL AND OPTIMIZER
model, optimizer = get_model(args.model_name, data, args.lr)
#model, optimizer = get_model('bert-base-uncased', data, 1e-5)

# TOKENIZE DATA AND RETRIEVE LABELS
domains, labels = tokenize_data(args.model_name, data)
#domains, labels = tokenize_data('bert-base-uncased', data)

# SPLIT DATA
train_loader, val_loader, test_loader = split_data(domains, labels, args.batch_size)
#train_loader, val_loader, test_loader = split_data(domains, labels, 64)

############################
######### TRAINING #########
############################

# Login into wandb
#wandb.login(key=str(args.wandb_key))
wandb.login(key="6b71979d3413a1673d7bb36423329ca11a52bcd9")

wandb.init(

    project = project_id,
    config = {
      "batch_size": args.batch_size,
      "lr": args.lr,
      "epochs": args.epochs,
      "model_name": args.model_name
    },
    name = args.model_name
)


'''
wandb.init(

    project = project_id,
    config = {
      "batch_size": 64,
      "lr": 1e-5,
      "epochs": 1,
      "model_name": 'bert-base-uncased'
    },
    name = 'bert-base-uncased'
)
'''
wandb.log({'frac': args.frac})
wandb.log({'batch_size': wandb.config.batch_size})
wandb.log({'lr': wandb.config.lr})
wandb.log({'epochs': wandb.config.epochs})
wandb.log({'model_name': wandb.config.model_name})

#start training run
start = datetime.now()
# Training loop
for epoch in range(wandb.config.epochs):
    model.train()
    for batch_idx, batch in enumerate(train_loader):
        input_ids, labels = [data.to(device) for data in batch]
        optimizer.zero_grad()
        output = model(input_ids, labels=labels)
        loss = output.loss
        if batch_idx % 1000 == 0:
            wandb.log({'train_batch_loss': loss})
        loss.backward()
        optimizer.step()

#end training run
end = datetime.now()
time = end - start
wandb.log({'total_training_time': str(time)})

############################
######## EVALUATION ########
############################

start = datetime.now()
model.eval()
correct = 0
total = 0
with torch.no_grad():
    for batch in test_loader:
        input_ids, labels = [data.to(device) for data in batch]
        output = model(input_ids)
        predictions = torch.argmax(output.logits, dim=1)
        correct += (predictions == labels).sum().item()
        total += labels.size(0)

accuracy = correct / total
wandb.log({'test_accuracy': accuracy})
print(f"Test Accuracy: {accuracy:.2%}")

#end training run
end = datetime.now()
time = end - start
wandb.log({'total_evaluation_time': str(time)})
wandb.run.finish()


#SAVE THE MODEL
path = f"/gcs/dga-trainer/model-ouput-{generate_uuid()}"
torch.save(model.state_dict(), path)
