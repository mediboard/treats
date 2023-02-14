import os
import pickle
import pandas as pd

from tqdm import tqdm

# TODO update this
STUDIES_PICKLE_FILE_PATH = "/Users/porterhunley/datasets/"

def get_outcome_and_intervention_modules(studies):
    outcome_modules = []
    intervention_modules = []
    study_ids = []
    for study in studies:
        if (
            "ResultsSection" in study["Study"]
            and "OutcomeMeasuresModule" in study["Study"]["ResultsSection"]
        ):
            outcome_modules.append(study["Study"]["ResultsSection"]["OutcomeMeasuresModule"])
            study_ids.append(study['Study']['ProtocolSection']['IdentificationModule']['NCTId'])

        elif "ArmsInterventionsModule" in study["Study"]["ProtocolSection"]:
            intervention_modules.append(study["Study"]["ProtocolSection"]["ArmsInterventionsModule"])

    return outcome_modules, intervention_modules, study_ids


def create_outcomes_table_helper(studies) -> pd.DataFrame:
    outcome_modules, intervention_modules, study_ids = get_outcome_and_intervention_modules(studies)

    outcome_df = {
        'study_id': [],
        'group_title': [],
        'group_no': [],
        'measure': [],
        'title': [],
        'value': [],
        'dispersion': [],
        'upper': [],
        'lower': [],
        'participants': []
    }

    for i, module in enumerate(outcome_modules):
        for measure in module['OutcomeMeasureList']['OutcomeMeasure']:
            try:
                overall_group_to_no = {}
                for denom in measure.get('OutcomeDenomList', {'OutcomeDenom': []})['OutcomeDenom']:
                    if denom.get('OutcomeDenomUnits', 'NA') == 'Participants':
                        for count in denom.get('OutcomeDenomCountList', {'OutcomeDenomCount': []})['OutcomeDenomCount']:
                            overall_group_to_no[count['OutcomeDenomCountGroupId']] = count['OutcomeDenomCountValue']

                group_to_title = {}
                for admin in measure.get('OutcomeGroupList', {'OutcomeGroup': []})['OutcomeGroup']:
                    group_to_title[admin.get('OutcomeGroupId', 'NA')] = admin.get('OutcomeGroupTitle', 'NA')

                # Sometimes the participants are just listed one time before all the others - not just in the class
                for group in measure.get('OutcomeClassList', {'OutcomeClass': []})['OutcomeClass']:

                    group_to_no = {}
                    for denom in group.get('OutcomeClassDenomList', {'OutcomeClassDenom': []})['OutcomeClassDenom']:
                        for count in denom.get('OutcomeClassDenomCountList', {'OutcomeClassDenomCount': []})['OutcomeClassDenomCount']:
                            group_to_no[count['OutcomeClassDenomCountGroupId']] = count['OutcomeClassDenomCountValue']

                    for cat in group.get('OutcomeCategoryList', {'OutcomeCategory': []})['OutcomeCategory']:
                        for outcome in cat['OutcomeMeasurementList']['OutcomeMeasurement']:
                            outcome_df['study_id'].append(study_ids[i])
                            outcome_df['group_title'].append(
                                group_to_title[outcome.get('OutcomeMeasurementGroupId', 'NA')])
                            outcome_df['group_no'].append(outcome.get('OutcomeMeasurementGroupId', 'NA'))
                            outcome_df['measure'].append(measure.get('OutcomeMeasureTitle', 'NA'))
                            outcome_df['value'].append(outcome.get('OutcomeMeasurementValue', 'NA'))
                            outcome_df['dispersion'].append(outcome.get('OutcomeMeasurementSpread', 'NA'))
                            outcome_df['upper'].append(outcome.get('OutcomeMeasurementUpperLimit', 'NA'))
                            outcome_df['lower'].append(outcome.get('OutcomeMeasurementLowerLimit', 'NA'))
                            outcome_df['participants'].append(
                                group_to_no.get(outcome.get('OutcomeMeasurementGroupId', 'NA'),
                                                None) or overall_group_to_no.get(
                                    outcome.get('OutcomeMeasurementGroupId', 'NA'), 'NA'))
                            outcome_df['title'].append(group.get('OutcomeClassTitle', 'NA'))

            except KeyError as e:
                continue

    outcome_table_df = pd.DataFrame.from_dict(outcome_df).reset_index(drop=True)
    return outcome_table_df


def get_study_ids(outcomes, connection):
    study_ids = pd.read_sql("select id as std_id, nct_id from temp_schema.studies", connection)
    merged_table = outcomes.merge(study_ids, left_on="study_id", right_on="nct_id")\
        .drop(columns=['study_id', 'nct_id'], axis=1)\
        .rename(columns={ 'std_id': 'study' })

    print(merged_table)

    return merged_table


def get_group_ids(outcomes, connection):
    groups = pd.read_sql("select id as grp_id, study as std_id, title as grp_title, study_id from temp_schema.groups", connection)
    merged_table = outcomes.merge(groups, left_on=["study", "group_title", "group_no"], right_on=["std_id", "grp_title", "study_id"])\
        .drop(columns=['group_title', 'group_no', 'std_id', 'study_id', 'grp_title'], axis=1)\
        .rename(columns={'grp_id': 'group' })

    print(merged_table)

    return merged_table


def get_measure_ids(outcomes, connection):
    study_ids = pd.read_sql("select id as msr_id, title as msr_title, study as std_id from temp_schema.measures", connection)
    merged_table = outcomes.merge(study_ids, left_on=["study", "measure"], right_on=["std_id", "msr_title"])\
        .drop(columns=['measure', 'std_id', 'msr_title'], axis=1)\
        .rename(columns={ 'msr_id': 'measure' })
        
    print(merged_table)

    return merged_table


# this takes in initial studies parsing
def create_outcomes_table():
    outcomes_table_dfs = []
    directory = STUDIES_PICKLE_FILE_PATH + 'clinical_trials/'
    print("Deserializing studies")
    for studies_data_pickle_file in tqdm(os.listdir(directory)):
        studies_file = os.path.join(directory, studies_data_pickle_file)
        with open(studies_file, 'rb') as f:
            studies_data = pickle.load(f)
            outcomes_table_df = create_outcomes_table_helper(studies=studies_data)
            outcomes_table_dfs.append(outcomes_table_df)

    outcomes_table = pd.concat(outcomes_table_dfs).reset_index(drop=True)
    return outcomes_table


def clean_outcomes_table(pre_cleaned_outcomes_table: pd.DataFrame) -> pd.DataFrame:
    outcome_db = pre_cleaned_outcomes_table.rename(columns={
        'participants': 'no_participants'
    })[['study', 'group', 'measure', 'title', 'value', 'dispersion', 'upper', 'lower', 'no_participants']]

    outcome_db['group'] = outcome_db['group'].apply(int)
    outcome_db['value'] = outcome_db['value'].apply(string2float)
    outcome_db['dispersion'] = outcome_db['dispersion'].apply(string2float)
    outcome_db['upper'] = outcome_db['upper'].apply(string2float)
    outcome_db['lower'] = outcome_db['lower'].apply(string2float)
    outcome_db['no_participants'] = outcome_db['no_participants'].apply(string2int)

    return outcome_db


def string2float(string):
    try:
        return float(string.replace(',', ''))
    except Exception as e:
        return float('nan')


def string2int(string):
    try:
        return int(string.replace(',', ''))
    except Exception as e:
        return -1


def upload_to_db(outcomes_table: pd.DataFrame, connection):
    outcomes_table.to_sql("outcomes", connection, index=False, if_exists="append", schema='temp_schema')


# requires studies + groups + measures
def outcomes_workflow(connection) -> None:
    outcomes_table = create_outcomes_table()

    print(outcomes_table)

    outcomes_table = get_study_ids(outcomes_table, connection)
    outcomes_table = get_group_ids(outcomes_table, connection)
    outcomes_table = get_measure_ids(outcomes_table, connection)

    outcomes_table = clean_outcomes_table(pre_cleaned_outcomes_table=outcomes_table)

    upload_to_db(outcomes_table, connection)

    print(outcomes_table)
    print(outcomes_table.keys())
    print(outcomes_table.iloc[100])


if __name__ == "__main__":
    connection = create_engine(DATABASE_URL).connect()
    outcomes_workflow()