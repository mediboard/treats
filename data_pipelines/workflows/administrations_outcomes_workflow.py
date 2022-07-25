import os
import pickle
import typing
import pandas as pd
from nltk.tokenize import word_tokenize, sent_tokenize

# TODO update this
STUDIES_PICKLE_FILE_PATH = "/Users/pauldittamo/src/mediboard/"


# TODO move to utils
def get_outcome_modules(studies):
    outcome_modules = []
    for study in studies:
        if 'OutcomeMeasuresModule' in study['Study']['ResultsSection']:
            outcome_modules.append(study['Study']['ResultsSection']['OutcomeMeasuresModule'])
            continue
        print('No Results: ', study['Study']['ProtocolSection']['IdentificationModule']['OfficialTitle'])

    return outcome_modules


def get_intervention_freq(studies):
    intervention_freq = {}
    for study in studies:
        try:
            for int_group in study['Study']['DerivedSection']['InterventionBrowseModule']['InterventionMeshList']['InterventionMesh']:
                # ensure key is all lower case
                key_term = int_group['InterventionMeshTerm'].lower()
                if key_term not in intervention_freq:
                    intervention_freq[key_term] = 0
                intervention_freq[key_term] += 1
        except KeyError as e:
            continue
    return intervention_freq


def create_outcomes_table_helper(studies):
    outcome_modules = get_outcome_modules(studies)
    admin_df = {
        'study_id': [],
        'group_id': [],
        'measure': [],
        'title': [],
        'description': [],
    }

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
                    admin_df['study_id'].append(study_id)
                    admin_df['group_id'].append(admin.get('OutcomeGroupId', 'NA'))
                    admin_df['measure'].append(measure.get('OutcomeMeasureTitle', 'NA'))
                    admin_df['title'].append(admin.get('OutcomeGroupTitle', 'NA'))
                    admin_df['description'].append(admin.get('OutcomeGroupDescription', 'NA'))
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

    admin_table_df = pd.DataFrame.from_dict(admin_df).reset_index(drop=True)
    outcome_table_df = pd.DataFrame.from_dict(outcome_df).reset_index(drop=True)
    return admin_table_df, outcome_table_df,


# this takes in initial studies parsing
def create_administrations_table():
    administrations_table_dfs = []
    outcomes_table_dfs = []
    intervention_freq = {}
    directory = STUDIES_PICKLE_FILE_PATH + 'clinical_trials/'
    for studies_data_pickle_file in os.listdir(directory):
        studies_file = os.path.join(directory, studies_data_pickle_file)
        print(f"Deserializing {studies_file}")
        with open(studies_file, 'rb') as f:
            studies_data = pickle.load(f)
            administrations_table_df, outcomes_table_df = create_outcomes_table_helper(studies=studies_data)
            intervention_freq.update(get_intervention_freq(studies=studies_data))
            administrations_table_dfs.append(administrations_table_df)
            outcomes_table_dfs.append(outcomes_table_df)

    administrations_table = pd.concat(administrations_table_dfs).reset_index(drop=True)
    outcomes_table = pd.concat(outcomes_table_dfs).reset_index(drop=True)
    return administrations_table, outcomes_table, intervention_freq


def clean_administrations_table(int_admins_sample: pd.DataFrame) -> pd.DataFrame:
    int_admins_sample['title_treats'] = [[z for z in y if z in x.lower()] for x, y in
                                         zip(int_admins_sample['title'], int_admins_sample['treatments'])]
    title_treats_df = int_admins_sample.groupby('study_id')['title_treats'].apply(list).reset_index()
    title_treats_df['title_treats_flat'] = [list(set([item for sublist in x for item in sublist])) for x in
                                            title_treats_df['title_treats']]
    with_title_treats = int_admins_sample.merge(title_treats_df[['study_id', 'title_treats_flat']], 'inner',
                                                ['study_id'])
    with_title_treats['subtracted'] = [[z for z in x if z not in y] for x, y in
                                       zip(with_title_treats['treatments'], with_title_treats['title_treats_flat'])]
    with_title_treats['added'] = with_title_treats['subtracted'] + with_title_treats['title_treats']
    adjusted_int_admins = with_title_treats.drop(columns=['title_treats', 'title_treats_flat', 'subtracted']).rename(
        columns={'added': 'adjusted'})
    adjusted_int_admins = adjusted_int_admins.drop_duplicates(['study_id', 'group_id', 'measure'])
    return adjusted_int_admins


def tokenize_sentence(sent):
    sents = sent_tokenize(sent)
    hd_tokens = [word_tokenize(x.lower()) for x in sents]
    tokens = [item for sublist in hd_tokens for item in sublist]
    return tokens


def str_contains_int(string, intervention_freq):
    sentence_set = set(string)
    intervention_freq_keys_set = set(intervention_freq.keys())
    treats_set = sentence_set.intersection(intervention_freq_keys_set)
    # TODO investigate when treats_set is empty - probably counts as dropped
    return list(treats_set)


def administrations_workflow() -> None:
    pre_cleaned_administrations_table, outcomes_table, intervention_freq = create_administrations_table()

    sampled_admins = pre_cleaned_administrations_table
    # can pkl and store these different steps
    token_titles = sampled_admins['title'].apply(lambda x: tokenize_sentence(x))
    token_desc = sampled_admins['description'].apply(lambda x: tokenize_sentence(x))
    sampled_admins['tokens'] = token_titles + token_desc
    sampled_admins['treatments'] = sampled_admins['tokens'].apply(lambda x: str_contains_int(x, intervention_freq))
    # TODO remove tokens column
    sampled_admins = clean_administrations_table(sampled_admins)
    print(sampled_admins)
    sampled_admins.to_pickle(STUDIES_PICKLE_FILE_PATH + 'adjusted_int_admins.pkl')


if __name__ == "__main__":
    administrations_workflow()
