import streamlit as st
import torch
from transformers import BertTokenizer, BertForSequenceClassification


labels = {'symmi':0, 'legit':1, 'ranbyus_v1':2, 'kraken_v1':3, 'not_dga':4, 'pushdo':5,
          'ranbyus_v2':6, 'zeus-newgoz':7, 'locky':8, 'corebot':9, 'dyre':10, 'shiotob':11,
          'proslikefan':12, 'nymaim':13, 'ramdo':14, 'necurs':15, 'tinba':16, 'vawtrak_v1':17,
          'qadars':18, 'matsnu':19, 'fobber_v2':20, 'alureon':21, 'bedep':22, 'dircrypt':23,
          'rovnix':24, 'sisron':25, 'cryptolocker':26, 'fobber_v1':27, 'chinad':28,
          'padcrypt':29, 'simda':30}

predict_labels = {v: k for k, v in labels.items()}

device = torch.device("cpu")
saved_model = 'bert_dga_classifier.pt'
num_labels = 31
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=num_labels)
model.to(device)  # Move the model to the CPU
model.load_state_dict(torch.load(saved_model, map_location=device))

st.title("BERT-powered DGA Classifier App")

text_input = st.text_area("Enter some text:")
if st.button("Analyze"):

    # tokenize domain
    tokenized_text = [tokenizer.encode(text_input, 
                                       truncation=True, 
                                       add_special_tokens=True, 
                                       max_length=20, 
                                       pad_to_max_length=True) ]
    print(tokenized_text)
    
    input = torch.LongTensor(tokenized_text)

    # Perform inference with your BERT model
    output = model(input)
    prediction = torch.argmax(output.logits, dim=1)
    result = predict_labels[prediction]

    st.write("Analysis Result:", result)