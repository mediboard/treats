import typing
import os
import os
import glob
import pandas as pd
import pickle
import torch
import transformers

from transformers import BertForTokenClassification,
from sqlalchemy import create_engine
from tqdm import tqdm


DATABASE_URL = os.environ.get('DATABASE_URL', default="postgresql://davonprewitt@localhost:5432")
MODEL_PATH = os.environ.get('MODEL_PATH', default="postgresql://davonprewitt@localhost:5432")


def get_ner_from_string(string, model):
    tokenized_sentence = tokenizer.encode(string)
    input_ids = torch.tensor([tokenized_sentence]).to(device)

    with torch.no_grad():
        output = model(input_ids)

    label_indices = np.argmax(output[0].to('cpu').numpy(), axis=2)
    tokens = tokenizer.convert_ids_to_tokens(input_ids.to('cpu').numpy()[0])

    # Join the split tokens
    new_tokens, new_labels = [], []
    for token, label_idx in zip(tokens, label_indices[0]):
        if token.startswith("##"):
            new_tokens[-1] = new_tokens[-1] + token[2:]

        else:
            new_labels.append(idx2tag[label_idx])
            new_tokens.append(token)

    return new_tokens, new_labels


def get_unique_treatments(string, model):
  tokens, labels = get_ner_from_string(string, model)
  treatments = []

  for i in range(len(tokens)):
    token = tokens[i]
    label = labels[i]

    if label == 'B':
      treatments.append(token)

    if label == 'I' and treatments:
      treatments[-1] += token
  
  return list(set(treatments))


def get_groups():
    groups = pd.read_sql("select id, title, description from groups")
    groups['text'] = 'Title: ' + groups['title'] + ' Description: ' + groups['description']

    return groups


def get_effect_groups():
    effect_groups = pd.read_sql("select id, title, description from effect_groups")
    effect_groups['text'] = 'Title: ' + effect_groups['title'] + ' Description: ' + effect_groups['description']

    return effect_groups


def load_ner_model():
    model = BertForTokenClassification.from_pretrained(
        "emilyalsentzer/Bio_ClinicalBERT",
        num_labels=len(tag2idx),
        output_attentions = False,
        output_hidden_states = False)

    model.load_state_dict(torch.load(MODEL_PATH))

    return model



def parse_treatments(groups: pd.DataFrame, effect_groups: pd.DataFrame):
    model = load_ner_model()
    tqdm.pandas()

    groups['treatments'] = groups['text'].progress_apply(lambda x: get_unique_treatments(x, model))
    effect_groups['treatments'] = effect_groups['text'].progress_apply(lambda x: get_unique_treatments(x, model))

    unique_treatments = pd.concat([groups['treatments'], effect_groups['treatments']], axis=0).drop_duplicates()

    db = create_engine(DATABASE_URL)
    unique_treatments.to_sql('treatments', db, index=False, if_exists='append')



def treatments_workflow():
    device = torch.device('cpu')
    if (torch.cuda.is_available()):
        device = torch.device("cuda")





