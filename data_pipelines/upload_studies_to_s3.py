"""Upload studies data to s3"""
import argparse
import json
import os
import pickle
from os import listdir
from os.path import join, isdir

# --------------------- #
from sqlalchemy import create_engine
from tqdm import tqdm
import boto3.session

DATA_PATH = os.environ.get('DATA_PATH', default="/Users/porterhunley/datasets")
DATABASE_URL = os.environ.get('DATABASE_URL', default="postgresql://davonprewitt@localhost:5432")

# TODO update w/ temp creds
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

sql_engine = create_engine(DATABASE_URL)
connection = sql_engine.connect()
# --------------------- #


CLIN_GOV_TRIALS_PATH = f'{DATA_PATH}/AllAPIJSON'
MAX_STUDIES_PARSE_BUFF_SIZE = 5000

def get_all_uploaded_ids():
     # Connect to DB
    query = '''select id from studies'''
    return [row[0] for row in sql_engine.execute(query)]

def download_data():
    os.system(f'rm -rf {DATA_PATH}/AllAPIJSON')
    os.system(f'curl -L https://ClinicalTrials.gov/AllAPIJSON.zip -O {DATA_PATH}')

def unzip_data():
    os.system(f'unzip {DATA_PATH}/AllAPIJSON.zip -d {DATA_PATH}/AllAPIJSON > /dev/null')
    os.system("rm -f AllAPIJSON.zip")

def clear_bucket():
    bucket = s3_resource.Bucket('medboard-data')
    bucket.objects.filter(Prefix="clinical_trials/").delete()


def save_results(obj, name, upload_to_cloud):
    with open(f'{DATA_PATH}/clinical_trials/{name}.pkl', "wb") as f:
        pickle.dump(obj, f)

    if upload_to_cloud:
        response = s3_client.put_object(Bucket='medboard-data',
                                        Key=f'clinical_trials/{name}.pkl',
                                        Body=pickle.dumps(obj))

        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            raise Exception('Failed to upload studies data pickle to s3')


def parse_clinical_trials(require_results=False, download_new=False, upload_to_cloud=False) -> None:
    """Parses clincial trials downloaded from https://clinicaltrials.gov/api/gui/ref/download_all"""
    if download_new:
        clear_bucket()
        # download_data()
        unzip_data()

    studies_parsed_buff = []
    errors_set = set()
    num_study_pickles_uploaded, dropped_no_results, dropped_not_unique, dropped_non_interventional, dropped_with_error = 0, 0, 0, 0, 0
    for directory in tqdm([f for f in listdir(CLIN_GOV_TRIALS_PATH) if isdir(join(CLIN_GOV_TRIALS_PATH, f))]):
        study_file_names = [f for f in listdir(CLIN_GOV_TRIALS_PATH + '/' + directory + '/')]

        for file in study_file_names:
            try:
                with open(CLIN_GOV_TRIALS_PATH + '/' +  directory + '/' + file) as f:
                    # Only add new data
                    data = json.load(f)['FullStudy']
                    optional_requirements = True

                    if require_results:
                        has_results = 'ResultsSection' in data['Study'] and 'OutcomeMeasuresModule' in data['Study'][
                            'ResultsSection']
                        if not has_results: 
                            dropped_no_results += 1
                        optional_requirements &= has_results

                    if optional_requirements:
                        studies_parsed_buff.append(data)
                        
            except Exception as e:
                errors_set.add(e)
                dropped_with_error += 1
                continue

            if len(studies_parsed_buff) >= MAX_STUDIES_PARSE_BUFF_SIZE:
                save_results(studies_parsed_buff, f'studies_{num_study_pickles_uploaded}', upload_to_cloud)

                num_study_pickles_uploaded += 1
                studies_parsed_buff = []

    save_results(studies_parsed_buff, f'studies_{num_study_pickles_uploaded + 1}', upload_to_cloud)

    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        raise Exception('Failed to upload studies data pickle to s3')

    print(f'Successfully uploaded {num_study_pickles_uploaded * MAX_STUDIES_PARSE_BUFF_SIZE + len(studies_parsed_buff)} clinical trials')

    if (require_results):
        print(f'Failed to parse {dropped_no_results} trials with no results')

    print(f'Failed to parse {dropped_non_interventional} non-interventional trials')
    print(f'Failed to parse {dropped_with_error} trials with error with errors: {errors_set}')


if __name__ == '__main__':
    parse_clinical_trials(require_results=False)
