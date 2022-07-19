"""Uploads studies_table to DB and pkl """
import typing
import os
import pandas as pd
import pickle

# TODO move this to a utils file
# --------------------- #
import boto3.session


STUDIES_PICKLE_FILE_PATH = "/Users/pauldittamo/src/mediboard/"


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


def update_studies_pkl() -> None:
    print(f"Downloading parsed studies from S3...")
    s3_bucket = s3_resource.Bucket('medboard-data')
    for obj in s3_bucket.objects.filter(Prefix='clinical_trials/studies_'):
        print(f'Downloading file {obj.key} to {STUDIES_PICKLE_FILE_PATH + obj.key}')
        s3_bucket.download_file(obj.key, STUDIES_PICKLE_FILE_PATH + obj.key)


def need_studies_downloaded() -> bool:
    # TODO implement
    return False


def create_studies_table_helper(studies: typing.List[dict]) -> pd.DataFrame:
    buffer = {
        'study_id': [], 'official_title': [], 'short_title': [], 'conditions': [],
        'verified_date': [], 'responsible_party': [], 'sponsor': [], 'type': [], 'description': [],
        'interventions': [], 'purpose': [], 'intervention_type': [], 'mesh_terms': [],
        'criteria': [], 'min_age': [], 'max_age': [], 'gender': []}
    for i, study in enumerate(studies):

        try:
            buffer['study_id'].append(study['Study']['ProtocolSection']['IdentificationModule']['NCTId'])
        except KeyError as e:
            buffer['study_id'].append('NA')

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

    return pd.DataFrame.from_dict(buffer).reset_index(drop=True)


def clean_studies_table(studies_table: pd.DataFrame) -> pd.DataFrame:
    db_studies_table = studies_table[
        ['study_id',
         'verified_date',
         'short_title',
         'official_title',
         'description',
         'responsible_party',
         'sponsor',
         'type',
         'purpose',
         'intervention_type',
         'min_age',
         'max_age',
         'gender',
         ]
    ].rename(
        columns={
            'study_id': 'id',
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

    db_studies_table = db_studies_table.set_index('id')

    month_dict = {
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

    db_studies_table = db_studies_table[
        ['upload_date',
         'short_title',
         'official_title',
         'description',
         'responsible_party',
         'sponsor',
         'type',
         'purpose',
         'intervention_type',
         'min_age',
         'min_age_units',
         'max_age',
         'max_age_units',
         'gender',
         ]
    ]
    db_studies_table['intervention_type'] = db_studies_table['intervention_type'].str.upper()
    db_studies_table['intervention_type'] = db_studies_table['intervention_type'].str.replace(' ', '_')
    db_studies_table['type'] = db_studies_table['type'].str.upper()
    db_studies_table['type'] = db_studies_table['type'].str.replace(' ', '_')
    db_studies_table['purpose'] = db_studies_table['purpose'].str.upper()
    db_studies_table['purpose'] = db_studies_table['purpose'].str.replace(' ', '_')
    db_studies_table['min_age_units'] = db_studies_table['min_age_units'].str.upper()
    db_studies_table['max_age_units'] = db_studies_table['max_age_units'].str.upper()
    db_studies_table['gender'] = db_studies_table['gender'].str.upper()

    return db_studies_table


def create_studies_table() -> pd.DataFrame:
    studies_table_dfs = []
    directory = STUDIES_PICKLE_FILE_PATH + 'clinical_trials/'
    for studies_data_pickle_file in os.listdir(directory):
        studies_file = os.path.join(directory, studies_data_pickle_file)
        print(f"Deserializing {studies_file}")
        with open(studies_file, 'rb') as f:
            studies_data = pickle.load(f)
            studies_table_df = create_studies_table_helper(studies=studies_data)
            studies_table_dfs.append(studies_table_df)

    studies_table = pd.concat(studies_table_dfs).reset_index(drop=True)
    return studies_table


def upload_to_db():
    return None


# this serializes studies_table object referenced by some workflows
def store_pre_cleaned_studies_table_pkl(studies_table: pd.DataFrame) -> None:
    studies_table.to_pickle(STUDIES_PICKLE_FILE_PATH + 'pre_cleaned_studies_table.pkl')


def studies_workflow(update_studies: bool) -> None:
    # TODO add versioning on studies uploads in S3 (check if latest)
    if update_studies or need_studies_downloaded():
        update_studies_pkl()
    studies_table = create_studies_table()
    store_pre_cleaned_studies_table_pkl(studies_table)
    studies_table = clean_studies_table(studies_table)
    print(studies_table)
    print(studies_table.keys())


# TODO add argparse to check if overwrite local studies pkl files
if __name__ == "__main__":
    studies_workflow(update_studies=False)
