"""writes conditions and studies_conditions tables"""
import pickle
import pandas as pd
import re

# TODO update this
STUDIES_PICKLE_FILE_PATH = "/Users/pauldittamo/src/mediboard/"


def load_pre_cleaned_studies_table() -> pd.DataFrame:
    with open(STUDIES_PICKLE_FILE_PATH + 'pre_cleaned_studies_table.pkl', 'rb') as f:
        studies_table = pickle.load(f)
    return studies_table


def get_conditions(studies_table: pd.DataFrame) -> pd.DataFrame:
    conditions = studies_table.explode('conditions')[['conditions', 'study_id']]
    conditions['alpha_num'] = conditions['conditions'].apply(lambda x: re.sub(r'[^a-zA-Z0-9 ]', '', x))
    conditions['sorted'] = conditions['alpha_num'].str.split().apply(sorted).apply(tuple)
    conditions_dict = {k: i for i, k in enumerate(conditions['sorted'].unique())}
    conditions['condition_id'] = conditions['sorted'].apply(lambda x: conditions_dict[x])
    conditions['l_conditions'] = conditions['conditions'].apply(lambda x: [x])
    return conditions


def most_common(lst):
    return max(set(lst), key=lst.count)


def create_conditions_table(conditions: pd.DataFrame) -> pd.DataFrame:
    conditions_table = pd.DataFrame(conditions.groupby('condition_id')['l_conditions'].apply(sum).apply(most_common))
    conditions_table = conditions_table.set_axis(['name'], axis=1, inplace=False)
    conditions_table = conditions_table.rename_axis(['id'], axis=0)
    return conditions_table


def create_study_conditions_table(conditions: pd.DataFrame) -> pd.DataFrame:
    study_conditions = conditions[['study_id', 'condition_id']].rename(columns={
        'study_id': 'study',
        'condition_id': 'condition'
    }).reset_index(drop=True)
    return study_conditions


# requires studies_workflow to write pre_cleaned studies_table to disk
def conditions_workflow() -> None:
    studies_table = load_pre_cleaned_studies_table()
    conditions = get_conditions(studies_table=studies_table)
    conditions_table = create_conditions_table(conditions=conditions)
    study_conditions_table = create_study_conditions_table(conditions=conditions)

    print(conditions_table)
    print(conditions_table.keys())

    print(study_conditions_table)
    print(study_conditions_table.keys())


if __name__ == "__main__":
    conditions_workflow()

