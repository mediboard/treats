import os
import pickle
import pandas as pd

# TODO update this
STUDIES_PICKLE_FILE_PATH = "/Users/pauldittamo/src/mediboard/"


def get_outcome_modules(studies):
    outcome_modules = []
    for study in studies:
        if 'OutcomeMeasuresModule' in study['Study']['ResultsSection']:
            outcome_modules.append(study['Study']['ResultsSection']['OutcomeMeasuresModule'])
            continue
        print('No Results: ', study['Study']['ProtocolSection']['IdentificationModule']['OfficialTitle'])

    return outcome_modules


def create_outcomes_table_helper(studies) -> pd.DataFrame:
    outcome_modules = get_outcome_modules(studies)

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
        study_id = studies[i]['Study']['ProtocolSection']['IdentificationModule']['NCTId']
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
                            outcome_df['study_id'].append(study_id)
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
                print(e)
                continue

    outcome_table_df = pd.DataFrame.from_dict(outcome_df).reset_index(drop=True)
    return outcome_table_df


# this takes in initial studies parsing
def create_outcomes_table():
    outcomes_table_dfs = []
    directory = STUDIES_PICKLE_FILE_PATH + 'clinical_trials/'
    for studies_data_pickle_file in os.listdir(directory):
        studies_file = os.path.join(directory, studies_data_pickle_file)
        print(f"Deserializing {studies_file}")
        with open(studies_file, 'rb') as f:
            studies_data = pickle.load(f)
            outcomes_table_df = create_outcomes_table_helper(studies=studies_data)
            outcomes_table_dfs.append(outcomes_table_df)

    outcomes_table = pd.concat(outcomes_table_dfs).reset_index(drop=True)
    with open(STUDIES_PICKLE_FILE_PATH + 'group_table.pkl', 'rb') as handle:
        groups_table = pickle.load(handle)

    groups_merge = groups_table.rename(columns={
        'title': 'group_title',
        'study': 'study_id',
        'study_id': 'group_no'
    })

    groups_merge = groups_merge.reset_index(level=0).rename(columns={
        'index': 'id',
    })

    merged = outcomes_table.merge(groups_merge[['group_title', 'study_id', 'id', 'group_no']], 'left', ['study_id', 'group_title', 'group_no']).drop_duplicates()
    outcomes_table = merged[~merged['id'].isna()]

    with open(STUDIES_PICKLE_FILE_PATH + 'measures_table.pkl', 'rb') as handle:
        measures_table = pickle.load(handle)

    measures_table = measures_table.reset_index(level=0).rename(columns={
        'index': 'id',
    })

    measures_merge = measures_table.rename(columns={
        'study': 'study_id',
        'title': 'measure'
    })[['id', 'study_id', 'measure']].drop_duplicates(['study_id', 'measure'])

    outcomes_table = outcomes_table.merge(measures_merge, 'left', ['study_id', 'measure'])

    return outcomes_table


def clean_outcomes_table(pre_cleaned_outcomes_table: pd.DataFrame) -> pd.DataFrame:
    outcome_db = pre_cleaned_outcomes_table.rename(columns={
        'study_id': 'study',
        'id_x': 'group',
        'id_y': 'measure',
        'measure': 'measure_title',
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


# requires groups + measures
def outcomes_workflow() -> None:
    pre_cleaned_outcomes_table = create_outcomes_table()
    outcomes_table = clean_outcomes_table(pre_cleaned_outcomes_table=pre_cleaned_outcomes_table)

    print(outcomes_table)
    print(outcomes_table.keys())
    print(outcomes_table.iloc[100])


if __name__ == "__main__":
    outcomes_workflow()
