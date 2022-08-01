"""writes effectsadministrations table"""
import pickle
import pandas as pd

# TODO update this
STUDIES_PICKLE_FILE_PATH = "/Users/pauldittamo/src/mediboard/"


def create_effectsadministrations_table() -> pd.DataFrame:

    with open(STUDIES_PICKLE_FILE_PATH + 'pre_cleaned_effects_groups_table.pkl', 'rb') as handle:
        pre_cleaned_effects_groups_table = pickle.load(handle)

    with open(STUDIES_PICKLE_FILE_PATH + 'study_treatments_table.pkl', 'rb') as handle:
        study_treatments_table = pickle.load(handle)

    study_treatments_table = study_treatments_table.rename(columns={
        'study': 'study_id'
    })

    effects_groups_treats = pre_cleaned_effects_groups_table.merge(study_treatments_table, on=["study_id"])

    effects_groups_treats = effects_groups_treats.rename(columns={
        'id': 'group'
    })[['group', 'treatment']]

    return effects_groups_treats


# requires study_treatments + precleaned_effectsgroups
def effectsadministrations_workflow() -> None:
    effectsadministrations_table = create_effectsadministrations_table()

    print(effectsadministrations_table)
    print(effectsadministrations_table.keys())
    print(effectsadministrations_table.iloc[1])


if __name__ == "__main__":
    effectsadministrations_workflow()
