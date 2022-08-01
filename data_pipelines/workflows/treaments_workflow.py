"""writes treatments and study_treatments table"""
import pickle
import pandas as pd


STUDIES_PICKLE_FILE_PATH = "/Users/pauldittamo/src/mediboard/"


def create_treatments_table() -> pd.DataFrame:
    with open(STUDIES_PICKLE_FILE_PATH + 'pre_cleaned_studies_table.pkl', 'rb') as f:
        studies_table = pickle.load(f)

    treatments = studies_table.explode('interventions')[['study_id', 'interventions']]
    treatments = pd.DataFrame(treatments.groupby('interventions')['study_id'].apply(list).apply(len)).reset_index()
    treatments_table = treatments.sort_values(by=['study_id'], ascending=False).rename(columns={
        'study_id': 'no_studies',
        'interventions': 'name'
    }).reset_index(drop=True)
    treatments_table['from_study'] = True
    return treatments_table


def create_study_treatments_table(treatments_table: pd.DataFrame) -> pd.DataFrame:

    treatments_table = treatments_table.rename_axis(['id'], axis=0)

    treatments_table = treatments_table.reset_index(level=0).rename(columns={
        'index': 'id',
    })

    with open(STUDIES_PICKLE_FILE_PATH + 'pre_cleaned_studies_table.pkl', 'rb') as f:
        studies_table = pickle.load(f)
    studies_conditions = studies_table[['study_id', 'interventions']].explode('interventions')

    study_treats = studies_conditions.merge(treatments_table[['id', 'name']].rename(columns={
        'name': 'interventions',
        'id': 'treatment'
    }), 'left', )[['study_id', 'treatment']].rename(columns={
        'study_id': 'study'
    })

    return study_treats


def combine_with_no_studies_treatments(treatments_table: pd.DataFrame) -> pd.DataFrame:
    # grab treatments from prod db with no_studies = -1
    # don't add treatments with old no_studies that now have studies + make sure id's don't overlap
    return treatments_table


def clean_treatments_table(treatments_table: pd.DataFrame) -> pd.DataFrame:
    treatments_table = treatments_table[['name', 'from_study', 'no_studies']].reset_index(drop=True)
    return treatments_table


# requires treatments with no_studies (analytics table?)
def treatments_workflow() -> None:
    treatments_table = create_treatments_table()
    # Don't combine treatments that have no studies (failed parsing)
    # treatments_table = combine_with_no_studies_treatments(treatments_table=treatments_table)
    treatments_table = clean_treatments_table(treatments_table=treatments_table)

    # used to make administrations table
    treatments_table.to_pickle(STUDIES_PICKLE_FILE_PATH + 'treatments_table.pkl')

    print(treatments_table)
    print(treatments_table.keys())
    print(treatments_table.iloc[1])

    study_treatments_table = create_study_treatments_table(treatments_table)

    # used with effectsadministrations
    study_treatments_table.to_pickle(STUDIES_PICKLE_FILE_PATH + 'study_treatments_table.pkl')

    print(study_treatments_table)
    print(study_treatments_table.keys())
    print(study_treatments_table.iloc[1])


if __name__ == "__main__":
    treatments_workflow()
