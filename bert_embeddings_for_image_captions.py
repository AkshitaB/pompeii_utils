# -*- coding: utf-8 -*-
"""BERT embeddings for Image captions.ipynb
"""

import torch
import numpy as np

# do I have GPU:
gpu_available = torch.cuda.is_available()
print(gpu_available)

# number of GPUs I have:
num = torch.cuda.device_count()
print(f'I have {num} GPUs')

# current device index
idx = torch.cuda.current_device()
print(f'My current device has index {idx}')

# GPU's name
name = torch.cuda.get_device_name(idx)
print(f'My GPU is {name}')

# Commented out IPython magic to ensure Python compatibility.
# %%bash
# pip install transformers

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)

CUDA_LAUNCH_BLOCKING=1
from transformers import *
#load the tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
#load the pretrained model
model = BertModel.from_pretrained('bert-base-uncased')
model.to(device)
model.eval()

from google.colab import drive
drive.mount('/content/drive')

def encode_sentence(sentence, model, embeddings):
  marked_sent = '[CLS] ' + sentence + ' [SEP]'

  tokenized_sent= tokenizer.tokenize(marked_sent)

  tokens_ids = tokenizer.convert_tokens_to_ids(tokenized_sent)
  
  #Truncating long sentences
  if len(tokens_ids) >= 512:
    tokens_ids = tokens_ids[:512]

  segments_ids = [1] * len(tokens_ids)
  tokens_tensor = torch.tensor([tokens_ids])
  segments_tensors = torch.tensor([segments_ids])

  with torch.no_grad():
    encoded_hidden_states, _ = model(tokens_tensor.to(device), segments_tensors.to(device))
  return torch.mean(encoded_hidden_states, axis=1)

File_names=["drive/My Drive/Colab Notebooks/english.txt"]
cnt=0
embeddings = []
for file in File_names:
  f = open(file)
  for line in f:
    sentence_rep = encode_sentence(line[1:-2], model, embeddings)
    embeddings.append(sentence_rep[0].cpu().numpy())
    cnt += 1
    
print("Transformed %d sentences", cnt)
print(np.array(embeddings).shape)
np.savetxt('drive/My Drive/Colab Notebooks/embeddings.txt',np.array(embeddings),fmt='%1.4e')

