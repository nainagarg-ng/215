
#PYTORCH
import torch

#TRANSFORMERS
from transformers import BertTokenizer
from transformers import BertForSequenceClassification

device = torch.device("cpu")
saved_model = "bert_dga_classifier.pt"
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=31)
model.to(device)  # Move the model to the CPU
model.load_state_dict(torch.load(saved_model, map_location=device))
model.to(device)
model.eval()
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
tokenizer.save_pretrained('./my_tokenizer')
model.save_pretrained('./my_model')