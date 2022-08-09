"""Upload studies data to s3"""
import json
import os
import pickle
from os import listdir
from os.path import join, isdir

# --------------------- #
import boto3.session

# TODO update this
STUDIES_PICKLE_FILE_PATH = "/Users/pauldittamo/src/mediboard/"

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

# --------------------- #


CLIN_GOV_TRIALS_PATH = os.path.expanduser('~') + '/src/AllAPIJSON/'
MAX_STUDIES_PARSE_BUFF_SIZE = 1000


# TODO to expand to adding in new studies w/o needed to re-parse everything
def parse_clinical_trials() -> None:
    """Parses clincial trials downloaded from https://clinicaltrials.gov/api/gui/ref/download_all"""
    studies_parsed_buff = []
    errors_set = set()
    num_study_pickles_uploaded, dropped_no_results, dropped_non_interventional, dropped_with_error = 0, 0, 0, 0
    for directory in [f for f in listdir(CLIN_GOV_TRIALS_PATH) if isdir(join(CLIN_GOV_TRIALS_PATH, f))]:
        study_file_names = [f for f in listdir(CLIN_GOV_TRIALS_PATH + directory + '/')]
        for file in study_file_names:
            try:
                with open(CLIN_GOV_TRIALS_PATH + directory + '/' + file) as f:
                    data = json.load(f)['FullStudy']
                    has_results = 'ResultsSection' in data['Study'] and 'OutcomeMeasuresModule' in data['Study'][
                        'ResultsSection']
                    interventions = [x.get('InterventionMeshTerm', 'NA') for x in
                                     data['Study']['DerivedSection']['InterventionBrowseModule'][
                                         'InterventionMeshList']['InterventionMesh']]
                    conditions = data['Study']['ProtocolSection']['ConditionsModule']['ConditionList']['Condition']
                    study_type = data['Study']['ProtocolSection']['DesignModule']['StudyType']
                    if has_results and interventions and conditions and (study_type == 'Interventional'):
                        studies_parsed_buff.append(data)
                    elif not has_results:
                        dropped_no_results += 1
                    else:
                        dropped_non_interventional += 1
            except Exception as e:
                # TODO fix this rn adds every error
                errors_set.add(e)
                dropped_with_error += 1
                continue

            if len(studies_parsed_buff) >= MAX_STUDIES_PARSE_BUFF_SIZE:
                print(f'Uploading studies_{num_study_pickles_uploaded}.pkl to s3')

                response = s3_client.put_object(Bucket='medboard-data',
                                                Key=f'clinical_trials/studies_{num_study_pickles_uploaded}.pkl',
                                                Body=pickle.dumps(studies_parsed_buff))

                if response['ResponseMetadata']['HTTPStatusCode'] != 200:
                    raise Exception('Failed to upload studies data pickle to s3')

                num_study_pickles_uploaded += 1
                studies_parsed_buff = []

    print(f'Uploading studies_{num_study_pickles_uploaded + 1}.pkl to s3')

    response = s3_client.put_object(Bucket='medboard-data',
                                    Key=f'clinical_trials/studies_{num_study_pickles_uploaded}.pkl',
                                    Body=pickle.dumps(studies_parsed_buff))

    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        raise Exception('Failed to upload studies data pickle to s3')

    print(f'Successfully uploaded {num_study_pickles_uploaded * MAX_STUDIES_PARSE_BUFF_SIZE + len(studies_parsed_buff)} clinical trials')
    print(f'Failed to parse {dropped_no_results} trials with no results')
    print(f'Failed to parse {dropped_non_interventional} non-interventional trials')
    print(f'Failed to parse {dropped_with_error} trials with error with errors: {errors_set}')


if __name__ == '__main__':
    parse_clinical_trials()
