"""writes groups table"""
import pickle
import pandas as pd

# TODO update this
STUDIES_PICKLE_FILE_PATH = "/Users/pauldittamo/src/mediboard/"


def create_groups_table() -> pd.DataFrame:
    with open(STUDIES_PICKLE_FILE_PATH + 'adjusted_int_admins.pkl', 'rb') as f:
        adjusted_int_admins = pickle.load(f)

    groups_table = adjusted_int_admins[
        ['study_id', 'group_id', 'title', 'description']].drop_duplicates().reset_index(drop=True)
    groups_table = groups_table.rename_axis(['id'], axis=0)

    return groups_table


def clean_groups_table(groups_table: pd.DataFrame) -> pd.DataFrame:
    groups_table = groups_table.rename(columns={
        'study_id': 'study',
        'group_id': 'study_id',
    })[['title', 'study_id', 'description', 'study']]
    return groups_table


# requires studies_workflow + adjusted_int_admins from administrations workflow
def groups_workflow() -> None:
    pre_cleaned_groups_table = create_groups_table()
    groups_table = clean_groups_table(pre_cleaned_groups_table)

    # used to make administrations + outcomes table
    groups_table.to_pickle(STUDIES_PICKLE_FILE_PATH + 'group_table.pkl')

    print(groups_table)
    print(groups_table.keys())
    print(groups_table.iloc[1])


if __name__ == "__main__":
    groups_workflow()