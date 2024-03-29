"""writes studies_table + download raw studies to disk"""
import typing
import os
import os
import glob
import pandas as pd
import pickle
import enum


# TODO move this to a utils file
# --------------------- #
import boto3.session

from sqlalchemy import create_engine
from tqdm import tqdm

DATA_PATH = os.environ.get('DATA_PATH', default="/Users/porterhunley/datasets")
DATABASE_URL = os.environ.get('DATABASE_URL', default="postgresql://meditreats:meditreats@localhost:5432/meditreats")

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

class who_masked(enum.Enum):
    PARTICIPANT='participant'
    INVESTIGATOR='investigator'
    OUTCOMES_ASSESSOR='outcomes assessor'
    CARE_PROVIDER='care provider'
    NA='NA'


def update_studies_pkl() -> None:
    print(f"Downloading parsed studies from S3...")
    s3_bucket = s3_resource.Bucket('medboard-data')
    for obj in s3_bucket.objects.filter(Prefix='clinical_trials/studies_'):
        print(f'Downloading file {obj.key} to {DATA_PATH + obj.key}')
        print(obj.key)
        s3_bucket.download_file(Key=obj.key, Filename=DATA_PATH + obj.key)


def create_studies_table_helper(studies: typing.List[dict]) -> pd.DataFrame:
    buffer = {
        'nct_id': [], 'official_title': [], 'short_title': [], 'conditions': [],
        'verified_date': [], 'responsible_party': [], 'sponsor': [], 'phase': [], 'type': [], 'description': [],
        'interventions': [], 'purpose': [], 'intervention_type': [], 'mesh_terms': [],
        'criteria': [], 'min_age': [], 'max_age': [], 'gender': [], 'completion_date': [], 'completion_date_type':[],
        'status': [], 'stopped_reason': [], 'design_allocation': [], 'design_masking': [], 'design_time_perspective': [],
        'who_masked': [], 'masking_description': [], 'model_description': []}
    for _, study in enumerate(studies):
        try:
            buffer['nct_id'].append(study['Study']['ProtocolSection']['IdentificationModule']['NCTId'])
        except KeyError as e:
            buffer['nct_id'].append('NA')

        try:
            buffer['official_title'].append(study['Study']['ProtocolSection']['IdentificationModule']['OfficialTitle'])
        except KeyError as e:
            buffer['official_title'].append('NA')

        try:
            buffer['short_title'].append(study['Study']['ProtocolSection']['IdentificationModule']['BriefTitle'])
        except KeyError as e:
            buffer['short_title'].append('NA')

        try:
            buffer['verified_date'].append(study['Study']['ProtocolSection']['StatusModule']['StatusVerifiedDate'])
        except KeyError as e:
            buffer['verified_date'].append('NA')

        try:
            buffer['responsible_party'].append(
                study['Study']['ProtocolSection']['SponsorCollaboratorsModule']['ResponsibleParty'][
                    'ResponsiblePartyInvestigatorFullName'])
        except KeyError as e:
            buffer['responsible_party'].append('NA')

        try:
            buffer['sponsor'].append(
                study['Study']['ProtocolSection']['SponsorCollaboratorsModule']['LeadSponsor']['LeadSponsorName'])
        except KeyError as e:
            buffer['sponsor'].append('NA')

        try:
            buffer['conditions'].append(
                study['Study']['ProtocolSection']['ConditionsModule']['ConditionList']['Condition'])
        except KeyError as e:
            buffer['conditions'].append('NA')

        try:
            phases = study['Study']['ProtocolSection']['DesignModule']['PhaseList']['Phase']
            if len(phases) > 1:
                phase = ' '.join(phases)
            else:
                phase = 'NA' if phases[0] == 'Not Applicable' else phases[0]
            buffer['phase'].append(phase)
        except KeyError as e:
            buffer['phase'].append('NA')

        try:
            buffer['type'].append(study['Study']['ProtocolSection']['DesignModule']['StudyType'])
        except KeyError as e:
            buffer['type'].append('NA')

        try:
            buffer['purpose'].append(
                study['Study']['ProtocolSection']['DesignModule']['DesignInfo'].get('DesignPrimaryPurpose', 'NA'))
        except KeyError as e:
            buffer['purpose'].append('NA')

        try:
            buffer['intervention_type'].append(
                study['Study']['ProtocolSection']['DesignModule']['DesignInfo'].get('DesignInterventionModel', 'NA'))
        except KeyError as e:
            buffer['intervention_type'].append('NA')

        try:
            buffer['mesh_terms'].append([x.get('ConditionMeshTerm', 'NA') for x in
                                         study['Study']['DerivedSection']['ConditionBrowseModule']['ConditionMeshList'][
                                             'ConditionMesh']])
        except KeyError as e:
            buffer['mesh_terms'].append([])

        try:
            buffer['description'].append(study['Study']['ProtocolSection']['DescriptionModule']['BriefSummary'])
        except KeyError as e:
            buffer['description'].append('NA')

        try:
            buffer['interventions'].append([x.get('InterventionMeshTerm', 'NA') for x in
                                            study['Study']['DerivedSection']['InterventionBrowseModule'][
                                                'InterventionMeshList']['InterventionMesh']])
        except KeyError as e:
            buffer['interventions'].append([])

        try:
            buffer['criteria'].append(study['Study']['ProtocolSection']['EligibilityModule']['EligibilityCriteria'])
        except KeyError as e:
            buffer['criteria'].append('NA')

        try:
            buffer['gender'].append(study['Study']['ProtocolSection']['EligibilityModule']['Gender'])
        except KeyError as e:
            buffer['gender'].append('NA')

        try:
            buffer['min_age'].append(study['Study']['ProtocolSection']['EligibilityModule']['MinimumAge'])
        except KeyError as e:
            buffer['min_age'].append('NA')

        try:
            buffer['max_age'].append(study['Study']['ProtocolSection']['EligibilityModule']['MaximumAge'])
        except KeyError as e:
            buffer['max_age'].append('NA')

        try:
            buffer['status'].append(study['Study']['ProtocolSection']['StatusModule']['OverallStatus'])
        except KeyError as e:
            buffer['status'].append('NA')
            
        try:
            buffer['completion_date'].append(study['Study']['ProtocolSection']['StatusModule']['PrimaryCompletionDateStruct']['PrimaryCompletionDate'])
        except KeyError as e:
            buffer['completion_date'].append('NA')
            
        try:
            buffer['completion_date_type'].append(study['Study']['ProtocolSection']['StatusModule']['PrimaryCompletionDateStruct']['PrimaryCompletionDateType'])
        except KeyError as e:
            buffer['completion_date_type'].append('NA')

        try:
            buffer['stopped_reason'].append(study['Study']['ProtocolSection']['StatusModule']['WhyStopped'])
        except KeyError as e:
            buffer['stopped_reason'].append('NA')

        try:
            buffer['design_allocation'].append(study['Study']['ProtocolSection']['DesignModule']['DesignInfo']['DesignAllocation'])
        except KeyError as e:
            buffer['design_allocation'].append('NA')
        
        try:
            buffer['design_masking'].append(study['Study']['ProtocolSection']['DesignModule']['DesignInfo']['DesignMaskingInfo']['DesignMasking'])
        except KeyError as e:
            buffer['design_masking'].append('NA')

        try:
            buffer['design_time_perspective'].append(study['Study']['ProtocolSection']['DesignModule']['DesignInfo']['DesignTimePerspectiveList']['DesignTimePerspective'])
        except KeyError as e:
            buffer['design_time_perspective'].append('NA')
            
        try:
            buffer['who_masked'].append(study['Study']['ProtocolSection']['DesignModule']['DesignInfo']['DesignMaskingInfo']['DesignWhoMaskedList']['DesignWhoMasked'])
        except KeyError as e:
            buffer['who_masked'].append('NA')
                        
        try:
            buffer['masking_description'].append(study['Study']['ProtocolSection']['DesignModule']['DesignInfo']['DesignMaskingInfo']['DesignMaskingDescription'])
        except KeyError as e:
            buffer['masking_description'].append('NA')
                                    
        try:
            buffer['model_description'].append(study['Study']['ProtocolSection']['DesignModule']['DesignInfo']['DesignInterventionModelDescription'])
        except KeyError as e:
            buffer['model_description'].append('NA')
            

    return pd.DataFrame.from_dict(buffer).reset_index(drop=True)


def clean_studies_table(studies_table: pd.DataFrame) -> pd.DataFrame:
    db_studies_table = studies_table[
        ['nct_id',
         'verified_date',
         'short_title',
         'official_title',
         'description',
         'responsible_party',
         'sponsor',
         'phase',
         'type',
         'purpose',
         'intervention_type',
         'min_age',
         'max_age',
         'gender',
         'completion_date',
         'completion_date_type',
         'status',
         'stopped_reason',
         'design_allocation',
         'design_masking',
         'design_time_perspective',
         'who_masked',
         'masking_description',
         'model_description']
    ].rename(
        columns={
            'verified_date': 'upload_date'
            }
    )

    db_studies_table['max_age_units'] = db_studies_table['max_age'].str.split(' ').apply(
        lambda x: x[1] if x != ['NA'] else 'NA')
    db_studies_table['max_age_units'] = db_studies_table['max_age_units'].apply(
        lambda x: x + 's' if (x != 'NA' and x[-1] != 's') else x)
    db_studies_table['max_age'] = db_studies_table['max_age'].str.split(' ').apply(
        lambda x: x[0] if x != ['NA'] else -1)

    db_studies_table['min_age_units'] = db_studies_table['min_age'].str.split(' ').apply(
        lambda x: x[1] if x != ['NA'] else 'NA')
    db_studies_table['min_age_units'] = db_studies_table['min_age_units'].apply(
        lambda x: x + 's' if (x != 'NA' and x[-1] != 's') else x)
    db_studies_table['min_age'] = db_studies_table['min_age'].str.split(' ').apply(
        lambda x: x[0] if x != ['NA'] else -1)

    db_studies_table['min_age'] = db_studies_table['min_age'].apply(int)
    db_studies_table['max_age'] = db_studies_table['max_age'].apply(int)

    month_dict = {
        'NA': -1,
        'January': 1,
        'February': 2,
        'March': 3,
        'April': 4,
        'May': 5,
        'June': 6,
        'July': 7,
        'August': 8,
        'September': 9,
        'October': 10,
        'November': 11,
        'December': 12,
    }

    db_studies_table['upload_date'] = \
        db_studies_table['upload_date'].str.split(' ').apply(lambda x: x[-1]) + '-' + \
        db_studies_table['upload_date'].str.split(' ').apply(lambda x: str(month_dict[x[0]])) + "-01"

    db_studies_table['upload_date'] = db_studies_table['upload_date'].apply(lambda x: None if 'NA' in x else x)
    
    db_studies_table['completion_date'] = \
        db_studies_table['completion_date'].str.split(' ').apply(lambda x: x[-1]) + '-' + \
        db_studies_table['completion_date'].str.split(' ').apply(lambda x: str(month_dict[x[0]])) + "-01"

    db_studies_table['completion_date'] = db_studies_table['completion_date'].apply(lambda x: None if 'NA' in x else x)

    db_studies_table['intervention_type'] = db_studies_table['intervention_type'].str.upper()
    db_studies_table['intervention_type'] = db_studies_table['intervention_type'].str.replace(' ', '_')
    db_studies_table['phase'] = db_studies_table['phase'].str.upper()
    db_studies_table['phase'] = db_studies_table['phase'].str.replace(' ', '_')
    db_studies_table['type'] = db_studies_table['type'].str.upper()
    db_studies_table['type'] = db_studies_table['type'].str.replace(' ', '_')
    db_studies_table['purpose'] = db_studies_table['purpose'].str.upper()
    db_studies_table['purpose'] = db_studies_table['purpose'].str.replace(' ', '_').str.replace('/', '_')
    db_studies_table['min_age_units'] = db_studies_table['min_age_units'].str.upper()
    db_studies_table['max_age_units'] = db_studies_table['max_age_units'].str.upper()
    db_studies_table['gender'] = db_studies_table['gender'].str.upper()
    db_studies_table['status'] = db_studies_table['status'].str.upper().str.replace(' ', '_').str.replace(',','')
    db_studies_table['completion_date_type'] = db_studies_table['completion_date_type'].str.upper().str.replace(' ', '_')

    db_studies_table['design_allocation'] = db_studies_table['design_allocation'].str.upper().str.replace(' ','_').str.replace('/','').str.replace('-','_')
    db_studies_table['design_masking'] = db_studies_table['design_masking'].apply(lambda x: 'None' if x == 'None (Open Label)' else x ).str.upper().str.replace(' ','_')
    db_studies_table['design_time_perspective'] = db_studies_table['design_time_perspective'].str.upper().str.replace(' ', '_')

    db_studies_table['who_masked'] = db_studies_table['who_masked'].apply(lambda x: [y.upper().replace(' ', '_') for y in x if x != 'NA'])
    db_studies_table['who_masked'] = db_studies_table['who_masked'].apply(lambda x: str(x).replace('[','{').replace(']', '}').replace("'", ""))

    # db_studies_table['observational_model'] = db_studies_table['observational_model'].str.upper().str.replace(' ', '_')

    return db_studies_table


def create_studies_table() -> pd.DataFrame:
    studies_table_dfs = []
    directory = DATA_PATH + '/clinical_trials/'
    for studies_data_pickle_file in tqdm(os.listdir(directory)):
        studies_file = os.path.join(directory, studies_data_pickle_file)
        with open(studies_file, 'rb') as f:
            studies_data = pickle.load(f)
            studies_table_df = create_studies_table_helper(studies=studies_data)
            studies_table_dfs.append(studies_table_df)

    studies_table = pd.concat(studies_table_dfs).reset_index(drop=True)
    return studies_table


def upload_to_db(studies_table: pd.DataFrame, connection):
    studies_table.to_sql('studies', connection, index=False, if_exists='append', schema='public')


def delete_old_studies():
    files = glob.glob(DATA_PATH + '/clinical_trials/*')
    for f in files:
        os.rmdir(f)


# this serializes studies_table object referenced by some workflows
def store_pre_cleaned_studies_table_pkl(studies_table: pd.DataFrame) -> None:
    studies_table.to_pickle(DATA_PATH + '/pre_cleaned_studies_table.pkl')


def studies_workflow(connection, update_studies: bool) -> None:
    # TODO add versioning on studies uploads in S3 (check if latest)
    if update_studies:
        studies_path = f'{DATA_PATH}/clinical_trials/'
        if not os.path.exists(studies_path):
            os.path.join(DATA_PATH, 'clinical_trials/')
            os.mkdir(studies_path)
        delete_old_studies()
        update_studies_pkl()

    studies_table = create_studies_table()
    store_pre_cleaned_studies_table_pkl(studies_table)
    studies_table = clean_studies_table(studies_table)
    studies_table['id'] = [i for i, x in enumerate(studies_table.index)] 
    upload_to_db(studies_table, connection)

    print(studies_table)
    print(studies_table.keys())
    print(studies_table.iloc[1])


# TODO add argparse to check if overwrite local studies pkl files
if __name__ == "__main__":
    connection = create_engine(DATABASE_URL).connect()
    studies_workflow(connection, update_studies=False)
