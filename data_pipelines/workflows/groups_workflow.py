import os
import pickle
import pandas as pd

from sqlalchemy import create_engine

import utils

DATA_PATH = os.environ.get("DATA_PATH", default="/Users/davonprewitt/datas")
DATABASE_URL = os.environ.get(
    "DATABASE_URL", default="postgresql://davonprewitt@localhost:5432"
)


def create_outcomes_table_helper(studies) -> pd.DataFrame:
    outcome_modules = utils.get_outcome_modules(studies)
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
                print(e)
                continue

    groups_table_df = pd.DataFrame.from_dict(group_df).reset_index(drop=True)
    return groups_table_df


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
    )[["title", "study_id", "description", "study"]]
    return groups_table


def upload_to_db(studies_table: pd.DataFrame):
    db = create_engine(DATABASE_URL)
    studies_table.to_sql("groups", db, index=False, if_exists="append")


def groups_workflow() -> None:
    pre_cleaned_groups_table = create_groups_table()
    groups_table = clean_groups_table(pre_cleaned_groups_table)
    upload_to_db(groups_table)

    print(groups_table)
    print(groups_table.keys())
    print(groups_table.iloc[1])


if __name__ == "__main__":
    groups_workflow()
