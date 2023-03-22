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
DATA_PATH = os.environ.get('DATA_PATH', default='/Users/porterhunley/datasets')

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


def get_groups(connection):
    print("Reading groups...")
    groups = pd.read_sql("select id, title, description from public.groups", connection)
    groups['text'] = 'Title: ' + groups['title'] + ' Description: ' + groups['description']

    return groups


def get_treatments(connection):
    print("Reading treatments...")
    treats = pd.read_sql('select id as treat_id, name as treatments from public.treatments', connection)

    return treats 


def get_effect_groups(connection):
    print("Reading effects groups...")
    effect_groups = pd.read_sql("select id, title, description from public.effectsgroups", connection)
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
    data.to_sql(table_name, connection, index=False, if_exists='append', )   


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


def parse_unique_treatments(treat_groups):
    print("Parsing unique treatments")
    unique_treats = treat_groups['treatments'].explode('treatments').unique()
    unique_treats = pd.DataFrame({'name': unique_treats})
    unique_treats['id'] = range(1, len(unique_treats) + 1)

    return unique_treats


def upload_treatments_workflow(connection):
    treat_groups = pd.read_pickle(DATA_PATH+'/all_treat_groups.pkl')

    treatments = parse_unique_treatments(treat_groups)
    upload_to_db(treatments, 'treatments', connection)

    treats = get_treatments(connection)

    group_admins = create_groups_admins(treat_groups, treats)
    upload_to_db(group_admins, 'administrations', connection)

    # effects_admins = create_effects_admins(treat_effect_groups, treats)
    # upload_to_db(effects_admins, 'effectsadministrations', connection)


if (__name__ == '__main__'):
    connection = create_engine(DATABASE_URL).connect()
    upload_treatments_workflow(connection)
