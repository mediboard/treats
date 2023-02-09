import os
import pickle
import pandas as pd
import utils

from sqlalchemy import create_engine


DATA_PATH = os.environ.get("DATA_PATH", default="/Users/davonprewitt/datas")
DATABASE_URL = os.environ.get("DATABASE_URL", default="postgresql://davonprewitt@localhost:5432")

def create_outcomes_table_helper(studies) -> pd.DataFrame:
    outcome_modules, intervention_modules = utils.get_outcome_and_intervention_modules(
        studies
    )
    group_df = {
        "study_id": [],
        "group_id": [],
        "title": [],
        "description": [],
    }

    for i, module in enumerate(outcome_modules):
        study_id = studies[i]["Study"]["ProtocolSection"]["IdentificationModule"][
            "NCTId"
        ]
        for measure in module["OutcomeMeasureList"]["OutcomeMeasure"]:
            try:
                for admin in measure.get("OutcomeGroupList", {"OutcomeGroup": []})[
                    "OutcomeGroup"
                ]:
                    group_df["study_id"].append(study_id)
                    group_df["group_id"].append(admin.get("OutcomeGroupId", "NA"))
                    group_df["title"].append(admin.get("OutcomeGroupTitle", "NA"))
                    group_df["description"].append(
                        admin.get("OutcomeGroupDescription", "NA")
                    )
            except KeyError as e:
                continue

    for i, module in enumerate(intervention_modules):
        study_id = studies[i]["Study"]["ProtocolSection"]["IdentificationModule"][
            "NCTId"
        ]
        try:
            for group in module.get("ArmGroupList", {"ArmGroup": []})["ArmGroup"]:
                group_df["study_id"].append(study_id)
                # Group IDs aren't present for studies without results
                group_df["group_id"].append("NA")
                group_df["title"].append(group.get("ArmGroupLabel", "NA"))
                group_df["description"].append(group.get("ArmGroupDescription", "NA"))
        except KeyError as e:
            print(e)
            continue

    groups_table_df = pd.DataFrame.from_dict(group_df).reset_index(drop=True)
    return groups_table_df


def add_study_id(table: pd.DataFrame, connection) -> pd.DataFrame:
    study_ids = pd.read_sql("select id as std_id, nct_id from studies", connection)
    merged_table = table.merge(study_ids, left_on="study", right_on="nct_id")\
        .drop(columns=['study'], axis=1)\
        .rename(columns={ 'std_id': 'study' })

    return merged_table[["id", "study", "title", "study_id", "description"]]


# this takes in initial studies parsing
def create_groups_table():
    groups_table_dfs = []
    directory = DATA_PATH + "/clinical_trials/"
    for studies_data_pickle_file in os.listdir(directory):
        studies_file = os.path.join(directory, studies_data_pickle_file)
        print(f"Deserializing {studies_file}")
        with open(studies_file, "rb") as f:
            studies_data = pickle.load(f)
            groups_table_df = create_outcomes_table_helper(studies=studies_data)
            groups_table_dfs.append(groups_table_df)

    groups_table = pd.concat(groups_table_dfs).reset_index(drop=True)
    return groups_table


def clean_groups_table(groups_table: pd.DataFrame) -> pd.DataFrame:
    groups_table = groups_table.rename(
        columns={
            "study_id": "study",
            "group_id": "study_id",
        }
    )[["title", "study_id", "description", "study"]].drop_duplicates()

    groups_table['id'] = range(1, len(groups_table) + 1)

    return groups_table


def upload_to_db(studies_table: pd.DataFrame, connection):
    studies_table.to_sql("groups", connection, index=False, if_exists="append")


def groups_workflow(connection) -> None:
    pre_cleaned_groups_table = create_groups_table()
    groups_table = clean_groups_table(pre_cleaned_groups_table)
    groups_table = add_study_id(groups_table, connection)

    upload_to_db(groups_table, connection)

    print(groups_table)
    print(groups_table.keys())
    print(groups_table.iloc[1])


if __name__ == "__main__":
    connection = create_engine(DATABASE_URL).connect()
    groups_workflow(connection)
