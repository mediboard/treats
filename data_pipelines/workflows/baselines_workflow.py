"""writes baselines_table + download raw studies to disk"""
import sys
import typing
import os
import os
import glob
import pandas as pd
import pickle

# TODO: Pipelines that read from the blob should have their own class
# --------------------- #
import boto3.session

from sqlalchemy import create_engine

DATA_PATH = os.environ.get('DATA_PATH', default="/Users/porterhunley/datasets")
DATABASE_URL = os.environ.get('DATABASE_URL', default="postgresql://davonprewitt@localhost:5432")


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
        print(f'Downloading file {obj.key} to {DATA_PATH + obj.key}')
        print(obj.key)
        s3_bucket.download_file(Key=obj.key, Filename=DATA_PATH + '/' + obj.key)

def create_baselines_table_helper(studies: typing.List[dict]) -> pd.DataFrame:
    df = {
        'study': [],
        'group_id': [],
        'base': [],
        'clss': [],
        'category': [],
        'param_type': [],
        'dispersion_type': [],
        'unit': [],
        'value': [],
        'spread': [],
        'upper': [],
        'lower': []
    }

    for study in studies:
        if ('ResultsSection' not in study['Study']):
            continue

        if ('BaselineCharacteristicsModule' not in study['Study']['ResultsSection']):
            continue

        study_id = study['Study']['ProtocolSection']['IdentificationModule']['NCTId']
        measures = study['Study']['ResultsSection']['BaselineCharacteristicsModule'].get('BaselineMeasureList', {'BaselineMeasure': []})['BaselineMeasure']

        for measure in measures:
            classes = measure.get('BaselineClassList', {'BaselineClass': []})['BaselineClass']

            for clss in classes:
                categories = clss.get('BaselineCategoryList', {'BaselineCategory': []})['BaselineCategory']

                for category in categories:
                    measurements = category.get('BaselineMeasurementList', {'BaselineMeasurement': []})['BaselineMeasurement']

                    for measurement in measurements:
                        df['study'].append(study_id)
                        df['group_id'].append(measurement.get('BaselineMeasurementGroupId', 'NA'))
                        df['base'].append(measure.get('BaselineMeasureTitle', 'NA'))
                        df['clss'].append(clss.get('BaselineClassTitle', 'NA'))
                        df['category'].append(category.get('BaselineCategoryTitle', 'NA'))
                        df['param_type'].append(measure.get('BaselineMeasureParamType', 'NA'))
                        df['dispersion_type'].append(measure.get('BaselineMeasureDispersionType', 'NA'))
                        df['unit'].append(measure.get('BaselineMeasureUnitOfMeasure', 'NA'))
                        df['value'].append(measurement.get('BaselineMeasurementValue', 'NA'))
                        df['spread'].append(measurement.get('BaselineMeasurementSpread', 'NA'))
                        df['upper'].append(measurement.get('BaselineMeasurementUpperLimit', 'NA'))
                        df['lower'].append(measurement.get('BaselineMeasurementLowerLimit', 'NA'))

    return pd.DataFrame(df)


def is_race_demographic(baseline_title):
    return 'race' in baseline_title.lower()


def is_sex_demographic(baseline_title):
    return ('gender' in baseline_title) or ('sex' in baseline_title)


def get_race_vals(baselines_table: pd.DataFrame) -> typing.Dict:
    race_base = baselines_table[baselines_table['base'].apply(is_race_demographic)]
    race_cat = race_base[race_base['category'] != 'NA']
    race_class = race_base[race_base['category'] == 'NA']
    race_class = race_class[race_class['clss'] != 'NA']

    race_cat['key_term'] = race_cat['category']
    race_class['key_term'] = race_class['clss']

    import re 
    # Rules based generally works pretty well
    white_list = ['white', 'caucasian', 'european']
    black_list = ['black', 'african', 'negro', 'AA']
    asian_list = ['asian', 'chinese', 'japanese']
    indian_list = ['indian', 'native american', 'alaska', 'north american']
    pacific_list = ['pacific', 'islander', 'hawaiian']

    # WHITE
    white_baseline = race_cat[race_cat['key_term'].str.contains('|'.join(white_list), flags=re.IGNORECASE, regex=True)]
    white_baseline = white_baseline[~white_baseline['key_term'].str.contains('|'.join(black_list+indian_list+pacific_list+['asian ' + ' asian' + ' asian ']), flags=re.IGNORECASE, regex=True)]
    white_vals = white_baseline['key_term'].unique()

    # BLACK
    black_baseline = race_cat[race_cat['key_term'].str.contains('|'.join(black_list), flags=re.IGNORECASE, regex=True)]
    black_baseline = black_baseline[~black_baseline['key_term'].str.contains('|'.join(white_list+indian_list+pacific_list+asian_list), flags=re.IGNORECASE, regex=True)]
    black_vals = black_baseline['key_term'].unique()

    # ASIAN
    asian_baseline = race_cat[race_cat['key_term'].str.contains('|'.join(asian_list), flags=re.IGNORECASE, regex=True)]
    asian_baseline = asian_baseline[~asian_baseline['key_term'].str.contains('|'.join(black_list+indian_list+pacific_list+white_list), flags=re.IGNORECASE, regex=True)]
    asian_vals = asian_baseline['key_term'].unique()

    # INDIAN
    indian_baseline = race_cat[race_cat['key_term'].str.contains('|'.join(indian_list), flags=re.IGNORECASE, regex=True)]
    indian_baseline = indian_baseline[~indian_baseline['key_term'].str.contains('|'.join(black_list+white_list+pacific_list+asian_list), flags=re.IGNORECASE, regex=True)]
    indian_vals = indian_baseline['key_term'].unique()

    # ISLANDER
    pacific_baseline = race_cat[race_cat['key_term'].str.contains('|'.join(pacific_list), flags=re.IGNORECASE, regex=True)]
    pacific_baseline = pacific_baseline[~pacific_baseline['key_term'].str.contains('|'.join(black_list+indian_list+white_list+asian_list), flags=re.IGNORECASE, regex=True)]
    pacific_vals = pacific_baseline['key_term'].unique()

    # COMBINE VALS
    race_dict = {
        **{k:'white' for k in white_vals},
        **{k:'black' for k in black_vals},
        **{k:'asian' for k in asian_vals},
        **{k:'indian' for k in indian_vals},
        **{k:'pacific' for k in pacific_vals}
    }

    return race_dict


def get_gender_vals(baselines_table: pd.DataFrame) -> typing.Dict:
    gender_baseline = baselines_table[baselines_table['base'].apply(is_sex_demographic)]
    gender_class = gender_baseline[(gender_baseline['clss']!='NA') & (gender_baseline['category']=='NA')]
    gender_cat = gender_baseline[gender_baseline['category']!='NA']

    gender_class['key_term'] = gender_class['clss']
    gender_cat['key_term'] = gender_cat['category']
    gender_rows = pd.concat([gender_class, gender_cat])

    import re 

    # FEMALE
    gender_rows['repl'] = gender_rows['key_term'].str.replace('female', '$$$', regex=True, flags=re.IGNORECASE)
    female_terms = gender_rows[gender_rows['repl'].str.contains(r'(\$\$\$|woman|girl)', flags=re.IGNORECASE) & 
        ~gender_rows['repl'].str.contains(r'(male|man|boy)', flags=re.IGNORECASE)]['key_term'].unique()

    # MALE
    male_terms = gender_rows[gender_rows['key_term'].str.contains('(male|man|boy)', case=False) &
        ~gender_rows['key_term'].str.contains('(female|woman|girl)', case=False)]['key_term'].unique()

    female_dict = {k:'female' for k in female_terms}
    male_dict = {k:'male' for k in male_terms}
    gender_dict = {**female_dict, **male_dict}

    return gender_dict 


def value_to_float(val):
    if val == 'NA' or val == 'Not reported':
        return float('nan')

    val = val.replace(',', '')
    try:
        return float(val)
    except ValueError:
        return float('nan')
    

def clean_baselines_table(baselines_table: pd.DataFrame) -> pd.DataFrame:
    race_dict = get_race_vals(baselines_table)
    gender_dict = get_gender_vals(baselines_table)

    # Get the keywords from the whole of baselines
    base_cat = baselines_table[baselines_table['category'] != 'NA']
    base_class = baselines_table[baselines_table['category'] == 'NA']
    base_class = base_class[base_class['clss'] != 'NA']

    base_cat['key_term'] = base_cat['category']
    base_class['key_term'] = base_class['clss']

    base_rows = pd.concat([base_cat, base_class])

    base_rows['race'] = base_rows['key_term'].map(race_dict)
    base_rows['gender'] = base_rows['key_term'].map(gender_dict)
    base_rows = base_rows.fillna('NA')

    base_rows['type'] = 'OTHER'
    base_rows['subtype'] = 'NA'

    base_rows.loc[base_rows['gender']!='NA', 'type'] = 'GENDER'
    base_rows.loc[base_rows['race'] != 'NA', 'type'] = 'RACE'

    base_rows.loc[base_rows['type']=='GENDER','subtype'] = base_rows[base_rows['type']=='GENDER']['gender'].str.upper()
    base_rows.loc[base_rows['type']=='RACE', 'subtype'] = base_rows[base_rows['type']=='RACE']['race'].str.upper()

    base_rows['base'] = base_rows['base'].fillna('NA')
    base_rows['clss'] = base_rows['clss'].fillna('NA')
    base_rows['category'] = base_rows['category'].fillna('NA')
    base_rows['param_type'] = base_rows['param_type'].fillna('NA')
    base_rows['unit'] = base_rows['unit'].fillna('NA')
    base_rows['sub_type'] = base_rows['subtype'].fillna('NA')
    base_rows['type'] = base_rows['type'].fillna('OTHER')
    base_rows['dispersion'] = base_rows['dispersion_type'].str.upper().str.replace(' ','_').str.replace('-','_')
    base_rows['param_type'] = base_rows['param_type'].str.upper().str.replace(' ', '_')

    base_rows['value'] = base_rows['value'].apply(value_to_float)
    base_rows['spread'] = base_rows['spread'].apply(value_to_float)
    base_rows['upper'] = base_rows['upper'].apply(value_to_float)
    base_rows['lower'] = base_rows['lower'].apply(value_to_float)

    return base_rows[['study','base','clss','category','param_type','dispersion',
                            'unit','value','spread','upper','lower', 'sub_type']]


def add_study_id(baselines_table: pd.DataFrame) -> pd.DataFrame:
    db = create_engine(DATABASE_URL)
    study_ids = pd.read_sql('select id, nct_id from studies', db.connect())
    merged_table = baselines_table.merge(study_ids, left_on='study', right_on='nct_id')

    return merged_table[['id','base','clss','category','param_type','dispersion',
        'unit','value','spread','upper','lower', 'sub_type']].rename(columns={
            'id': 'study'
        })


def store_pre_cleaned_baselines_table_pkl(baselines_table: pd.DataFrame) -> None:
    baselines_table.to_pickle(DATA_PATH + 'pre_cleaned_baselines_table.pkl')


def create_baselines_table() -> pd.DataFrame:
    baselines_table_dfs = []
    directory = DATA_PATH + '/clinical_trials/'

    for studies_data_pickle_file in os.listdir(directory):
        studies_file = os.path.join(directory, studies_data_pickle_file)
        print(f"Deserializing {studies_file}")

        with open(studies_file, 'rb') as f:
            studies_data = pickle.load(f)
            baselines_table_df = create_baselines_table_helper(studies=studies_data)
            baselines_table_dfs.append(baselines_table_df)

    studies_table = pd.concat(baselines_table_dfs).reset_index(drop=True)
    return studies_table


def delete_old_studies():
    files = glob.glob(DATA_PATH + '/clinical_trials/*')
    for f in files:
        os.rmdir(f)

        
def upload_to_db(baselines_table: pd.DataFrame):
    # studies_table = studies_table.rename_axis('id').reset_index()
    db = create_engine(DATABASE_URL)
    baselines_table.to_sql('baselines', db, index=False, if_exists='append')


def baselines_workflow(update_studies=False):
    if update_studies:
        studies_path = f'{DATA_PATH}/clinical_trials/'

        if not os.path.exists(studies_path):
            os.path.join(DATA_PATH, '/clinical_trials/')
            os.mkdir(studies_path)

        delete_old_studies()
        update_studies_pkl()

    baselines_table = create_baselines_table()
    store_pre_cleaned_baselines_table_pkl(baselines_table)
    baselines_table = clean_baselines_table(baselines_table)
    baselines_table = add_study_id(baselines_table)
    upload_to_db(baselines_table)


if __name__ == '__main__':
    baselines_workflow()
