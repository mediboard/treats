"""creates study treatments table, requires: studies table, treatments table"""
import pandas as pd
import boto3
import pickle
import boto3.session
import typing
import os

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

DATA_PATH = os.environ.get('DATA_PATH', default="/Users/porterhunley/datasets")
DATABASE_URL = os.environ.get('DATABASE_URL', default="postgresql://davonprewitt@localhost:5432")

cred = boto3.Session().get_credentials()
ACCESS_KEY = cred.access_key
SECRET_KEY = cred.secret_key
SESSION_TOKEN = cred.token

DB_ENGINE = create_engine(DATABASE_URL)

s3_resource = boto3.resource('s3',
                             aws_access_key_id=ACCESS_KEY,
                             aws_secret_access_key=SECRET_KEY,
                             aws_session_token=SESSION_TOKEN)

s3_client = boto3.client('s3',
                         aws_access_key_id=ACCESS_KEY,
                         aws_secret_access_key=SECRET_KEY,
                         aws_session_token=SESSION_TOKEN)


def create_study_treats_table() -> pd.DataFrame:
    study_treatment_dfs = []
    directory = DATA_PATH + '/clinical_trials/'
    for studies_data_pickle_file in os.listdir(directory):
        studies_file = os.path.join(directory, studies_data_pickle_file)
        print(f"Deserializing {studies_file}")
        with open(studies_file, 'rb') as f:
            studies_data = pickle.load(f)
            study_treatments_df = parse_study_treatments(studies=studies_data)
            study_treatment_dfs.append(study_treatments_df)

    studies_treats_table = pd.concat(study_treatment_dfs).reset_index(drop=True)
    return studies_treats_table


def parse_study_treatments(studies: typing.List[dict]) -> pd.DataFrame:
    study_treats = {
        'study_id': [],
        'treatments': []
    }

    for study in studies:
        study_treats['study_id'].append(study['Study']['ProtocolSection']['IdentificationModule']['NCTId'])

        try: 
            study_treats['treatments'].append([x.get('InterventionMeshTerm', 'NA') for x in study['Study']['DerivedSection']['InterventionBrowseModule']['InterventionMeshList']['InterventionMesh']])
        except KeyError as e:
            study_treats['treatments'].append([])

    return pd.DataFrame.from_dict(study_treats).reset_index(drop=True)


def get_study_id(study_treats: pd.DataFrame) -> pd.DataFrame:
    db = create_engine(DATABASE_URL)
    study_ids = pd.read_sql("select id as std_id, nct_id from studies", db.connect())
    merged_table = study_treats.merge(study_ids, left_on="study_id", right_on="nct_id")\
        .drop(columns=['study_id', 'nct_id'], axis=1)\
        .rename(columns={ 'std_id': 'study' })

    return merged_table


# def get_treatment_id(study_treats: pd.DataFrame) -> pd.DataFrame:

#     return merged_table


def upload_to_db(data: pd.DataFrame, table_name):
    data.to_sql(table_name, DB_ENGINE, index=False, if_exists='append')   


def fill_in_treatments(study_treats: pd.DataFrame) -> pd.DataFrame:
    study_treats['treatments'] = study_treats['treatments'].str.lower()

    treatments = pd.read_sql("select id as treat_id, name from treatments", DB_ENGINE.connect())
    merged_table = study_treats.merge(treatments, how='left', left_on="treatments", right_on="name")\
        .drop(columns=['name'], axis=1)\
        .rename(columns={ 
            'treatments': 'treat_name',
            'treat_id': 'treatment' })

    last_id = treatments['treat_id'].max()
    last_id = 0 if not pd.notnull(treatments['treat_id']).any() else int(last_id)

    print("last treatment id " + str(last_id))

    nan_treats = merged_table[merged_table['treatment'].isna()]

    new_treatments = nan_treats['treat_name'].str.lower().drop_duplicates().to_frame()
    new_treatments['id'] = range(last_id + 1, last_id + 1 + len(new_treatments))
    new_treatments = new_treatments.rename(columns={'treat_name': 'name'})

    print("uploading new treatments")

    upload_to_db(new_treatments, 'treatments')

    # Do it again
    treatments = pd.read_sql("select id as treat_id, name from treatments", DB_ENGINE.connect())
    merged_table = study_treats.merge(treatments, how='left', left_on="treatments", right_on="name")\
        .drop(columns=['name', 'treatments'], axis=1)\
        .rename(columns={'treat_id': 'treatment'})

    print(merged_table)

    return merged_table


def study_treatments_workflow():
    print("creating table...")
    study_treats_table = create_study_treats_table()

    print("adding in treatments...")
    study_treats_table = fill_in_treatments(study_treats_table.explode('treatments').dropna())

    print("adding in study id...")
    study_treats_table = get_study_id(study_treats_table)

    print("uploading to db...")
    upload_to_db(study_treats_table, 'study_treatments')


if __name__ == '__main__':
    study_treatments_workflow()

