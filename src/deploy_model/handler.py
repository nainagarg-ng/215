from ts.torch_handler.base_handler import BaseHandler
import os
import logging

#PYTORCH
import torch

#PANDAS
#import pandas as pd

#TRANSFORMERS
from transformers import BertTokenizer
from transformers import BertForSequenceClassification

logger = logging.getLogger(__name__)

labels = {'symmi':0, 'legit':1, 'ranbyus_v1':2, 'kraken_v1':3, 'not_dga':4, 'pushdo':5,
          'ranbyus_v2':6, 'zeus-newgoz':7, 'locky':8, 'corebot':9, 'dyre':10, 'shiotob':11,
          'proslikefan':12, 'nymaim':13, 'ramdo':14, 'necurs':15, 'tinba':16, 'vawtrak_v1':17,
          'qadars':18, 'matsnu':19, 'fobber_v2':20, 'alureon':21, 'bedep':22, 'dircrypt':23,
          'rovnix':24, 'sisron':25, 'cryptolocker':26, 'fobber_v1':27, 'chinad':28,
          'padcrypt':29, 'simda':30}

predict_labels = {v: k for k, v in labels.items()}


class MyHandler(BaseHandler):

    def __init__(self):
        super(MyHandler, self).__init__()
        self.initialized = False
        self.context = None
        self.model = None
        self.device = torch.device("cpu")
        self.num_labels = 31
        self.domains = None

    def initialize(self, context):

        #context contains model server system properties
        self.manifest = context.manifest
        properties = context.system_properties
        model_dir = properties.get("model_dir")
        logger.info(f"model_dir={model_dir}")
        #serialized bert dga classifier
        serialized_file = self.manifest['model']['serializedFile']
        model_pt_path = os.path.join(model_dir, serialized_file)
 
        #make sure is path
        if not os.path.isfile(model_pt_path):
            raise RuntimeError("Missing the model.pt file")
        
        #download bert model
        model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=self.num_labels)
        model.to(self.device)

        #load fine-tuned state dict
        model.load_state_dict(torch.load(model_pt_path, map_location=self.device))
        self.model = model
        self.model.to(self.device)
        self.model.eval()

        self.initialized = True


    def preprocess(self, request):
        
        """Tokenize the input text using the suitable tokenizer and convert it to tensor

        Args:
            requests: A list containing a dictionary, might be in the form
            of [{'body': json_file}] or [{'data': json_file}]
        """
        logger.info(f"REQUEST_MADE={request}")
        # unpack the data
        self.domains = [r.get("domain") for r in request]
        ''''
        if request[0].get("body"):
            body = request[0].get("body")
            #body = body.decode('utf-8')
            logger.info(f"REQUEST_MADE_DECODED={body}")
            self.domains = [domain.get("domain") for domain in body]
            logger.info(f"DOMAINS={self.domains}")
        elif request[0].get("data"):
            data = request[0].get("data")
            #data = data.decode('utf-8')
            logger.info(f"REQUEST_MADE_DECODED={data}")
            self.domains = [domain.get("domain") for domain in data]
            logger.info(f"DOMAINS={self.domains}")
        '''

        # tokenize the texts
        tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        tokenized_text = [tokenizer.encode(domain, 
                                           truncation=True, 
                                           add_special_tokens=True, 
                                           max_length=20, 
                                           pad_to_max_length=True) for domain in self.domains]
        inputs = torch.LongTensor(tokenized_text)

        return inputs

    def inference(self, inputs):
        # Perform inference with the model
        outputs = self.model(inputs)
        return outputs

    def postprocess(self, results):
        # Implement any necessary postprocessing logic; get preds
        prediction = torch.argmax(results.logits, dim=1)
        result = [predict_labels[pred.item()] for pred in prediction]
        output = [{d:r} for d,r in zip(self.domains, result)]
        return output