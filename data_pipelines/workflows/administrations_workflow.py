"""writes administrations table"""
import pickle
import pandas as pd

# TODO update this
STUDIES_PICKLE_FILE_PATH = "/Users/pauldittamo/src/mediboard/"


def clean_admin_table(adjusted_int_admins: pd.DataFrame) -> pd.DataFrame:

    with open(STUDIES_PICKLE_FILE_PATH + 'treatments_table.pkl', 'rb') as handle:
        treatment_table = pickle.load(handle)

    expl_admins = adjusted_int_admins.explode('adjusted')
    expl_admins['adjusted'] = expl_admins['adjusted'].str.capitalize()

    treatment_merge = treatment_table.rename_axis(['id'], axis=0).rename(columns={
        'name': 'adjusted'
    })

    treatment_merge['treatment'] = treatment_merge.index

    admins_treats = expl_admins.merge(treatment_merge[['adjusted', 'treatment']], 'left', ['adjusted'])

    # losing a little less than 1% but still not good practice
    admins_treats = admins_treats[~admins_treats['treatment'].isna()]

    with open(STUDIES_PICKLE_FILE_PATH + 'group_table.pkl', 'rb') as handle:
        groups_table = pickle.load(handle)

    groups_table['group'] = groups_table.index

    groups_merge = groups_table.rename(columns={
        'study_id': 'group_id',
        'study': 'study_id'
    })[['title', 'group_id', 'study_id', 'group']]

    admin_db = admins_treats.merge(groups_merge, 'left', ['study_id', 'group_id', 'title'])[
        ['group', 'treatment', 'description']].reset_index(drop=True).drop_duplicates()

    admin_db['treatment'] = admin_db['treatment'].apply(int)

    return admin_db


# requires adjusted_administrations + treatments + groups table
def administrations_workflow() -> None:
    with open(STUDIES_PICKLE_FILE_PATH + 'adjusted_int_admins.pkl', 'rb') as handle:
        adjusted_int_admins = pickle.load(handle)

    admin_table = clean_admin_table(adjusted_int_admins)

    print(admin_table)
    print(admin_table.keys())
    print(admin_table.iloc[1])


if __name__ == "__main__":
    administrations_workflow()
