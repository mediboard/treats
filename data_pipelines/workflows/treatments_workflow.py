"""creates treatments table, administrations table, and effectadministrations table"""
import typing
import os
import os
import glob
import pandas as pd
import numpy as np
import pickle
import boto3
import torch
import transformers

from transformers import BertForTokenClassification, BertTokenizer
from sqlalchemy import create_engine
from tqdm import tqdm


DATABASE_URL = os.environ.get('DATABASE_URL', default="postgresql://meditreats@localhost:5432")
MODEL_PATH = os.environ.get('MODEL_PATH', default="/Users/porterhunley/models")

cred = boto3.Session().get_credentials()
ACCESS_KEY = cred.access_key
SECRET_KEY = cred.secret_key
SESSION_TOKEN = cred.token

s3_resource = boto3.resource('s3',
                             aws_access_key_id=ACCESS_KEY,
                             aws_secret_access_key=SECRET_KEY,
                             aws_session_token=SESSION_TOKEN)

s3_client = boto3.client('s3',
                         aws_access_key_id=ACCESS_KEY,
                         aws_secret_access_key=SECRET_KEY,
                         aws_session_token=SESSION_TOKEN)


def get_device():
    device = torch.device('cpu')
    if (torch.cuda.is_available()):
        device = torch.device("cuda")

    return device


DEVICE = get_device()


tag2idx = {
    'B': 2,
    'I': 0,
    'O': 1,
    'PAD': 3
}
idx2tag = {v: k for k,v in tag2idx.items()}

def get_ner_from_string(string, model, tokenizer):
    tokenized_sentence = tokenizer.encode(string)
    input_ids = torch.tensor([tokenized_sentence]).to(DEVICE)

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


def get_unique_treatments(string, model, tokenizer):
  tokens, labels = get_ner_from_string(string, model, tokenizer)
  treatments = []

  for i in range(len(tokens)):
    token = tokens[i]
    label = labels[i]

    if label == 'B':
      treatments.append(token)

    if label == 'I' and treatments:
      treatments[-1] += token
  
  return list(set(treatments))


def get_groups(connection):
    print("Reading groups...")
    groups = pd.read_sql("select id, title, description from groups", connection)
    groups['text'] = 'Title: ' + groups['title'] + ' Description: ' + groups['description']

    return groups


def get_treatments(connection):
    print("Reading treatments...")
    treats = pd.read_sql('select id as treat_id, name as treatments from treatments', connection)

    return treats 


def get_effect_groups(connection):
    print("Reading effects groups...")
    effect_groups = pd.read_sql("select id, title, description from effectsgroups", connection)
    effect_groups['text'] = 'Title: ' + effect_groups['title'] + ' Description: ' + effect_groups['description']

    return effect_groups


def download_model():
    s3_client.download_file('medboard-data', 'models/ClinicalBertNERModel.pt', MODEL_PATH+'/ClinicalBertNERModel.pt')


def load_ner_model():
    print("Loading NER model...")
    model_path = f'{MODEL_PATH}/ClinicalBertNERModel.pt'
    if (not os.path.exists(model_path)):
        download_model()

    model = BertForTokenClassification.from_pretrained(
        "emilyalsentzer/Bio_ClinicalBERT",
        num_labels=len(tag2idx),
        output_attentions = False,
        output_hidden_states = False)

    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))

    return model


def load_tokenizer():
    print("Loading tokenizer...")
    return BertTokenizer.from_pretrained('emilyalsentzer/Bio_ClinicalBERT', do_lower_case=True)


def upload_to_db(data: pd.DataFrame, table_name, connection):
    data.to_sql(table_name, connection, index=False, if_exists='append')   


def parse_treatments(groups: pd.DataFrame, effect_groups: pd.DataFrame):
    # TODO - this should be batched
    model = load_ner_model()
    tokenizer = load_tokenizer()

    tqdm.pandas()

    groups['treatments'] = groups['text'].progress_apply(lambda x: get_unique_treatments(x, model, tokenizer))
    print(groups['treatments'])
    effect_groups['treatments'] = effect_groups['text'].progress_apply(lambda x: get_unique_treatments(x, model, tokenizer))

    unique_treatments = pd.concat([groups['treatments'], effect_groups['treatments']], axis=0)\
        .explode('treatments')\
        .str.lower()\
        .drop_duplicates()\
        .to_frame()

    unique_treatments = unique_treatments.rename(columns={ 'treatments': 'name'})
    unique_treatments['id'] = range(1, len(unique_treatments) + 1)
    unique_treatments = unique_treatments.reset_index(drop=True)

    return unique_treatments, groups, effect_groups


def create_groups_admins(groups: pd.DataFrame, treats):
    print("Creating admins table")
    exploded = groups.explode('treatments')

    admins = exploded[['id', 'treatments']].merge(treats, on='treatments').drop_duplicates()

    admins['new_id'] = range(1, len(admins) + 1)

    admins = admins[['id', 'new_id', 'treat_id']].rename(columns = {
        'id': 'group',
        'new_id': 'id',
        'treat_id': 'treatment'
    })

    return admins


def create_effects_admins(effect_groups: pd.DataFrame, treats):
    print("Creating effects admins table")
    exploded = effect_groups.explode('treatments')

    admins = exploded[['id', 'treatments']].merge(treats, on='treatments').drop_duplicates()

    admins['new_id'] = range(1, len(admins) + 1)

    admins = admins[['id', 'new_id', 'treat_id']].rename(columns = {
        'id': 'group',
        'new_id': 'id',
        'treat_id': 'treatment'
    })

    return admins


def run_treatments_workflow(connection):
    groups = get_groups(connection)
    effect_groups = get_effect_groups(connection)

    treats, treat_groups, treat_effect_groups = parse_treatments(groups, effect_groups)
    upload_to_db(treats, 'treatments', connection)

    # Need to refresh with id
    treats = get_treatments(connection)

    group_admins = create_groups_admins(treat_groups, treats)
    upload_to_db(group_admins, 'administrations', connection)

    effects_admins = create_effects_admins(treat_effect_groups, treats)
    upload_to_db(effects_admins, 'effectsadministrations', connection)



if (__name__ == '__main__'):
    connection = create_engine(DATABASE_URL).connect()
    run_treatments_workflow(connection)
