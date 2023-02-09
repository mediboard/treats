"""writes conditions and studies_conditions tables"""
import os
import pickle
import pandas as pd
import re

from sqlalchemy import create_engine

DATA_PATH = os.environ.get("DATA_PATH", default="/Users/davonprewitt/data")
DATABASE_URL = os.environ.get(
    "DATABASE_URL", default="postgresql://davonprewitt@localhost:5432"
)


def load_pre_cleaned_studies_table() -> pd.DataFrame:
    with open(DATA_PATH + "/pre_cleaned_studies_table.pkl", "rb") as f:
        studies_table = pickle.load(f)
    return studies_table


def get_conditions(studies_table: pd.DataFrame) -> pd.DataFrame:
    conditions = studies_table.explode("conditions")[["conditions", "study_id"]]
    conditions["alpha_num"] = conditions["conditions"].apply(
        lambda x: re.sub(r"[^a-zA-Z0-9 ]", "", x)
    )
    conditions["sorted"] = (
        conditions["alpha_num"].str.split().apply(sorted).apply(tuple)
    )
    conditions_dict = {k: i for i, k in enumerate(conditions["sorted"].unique())}
    conditions["condition_id"] = conditions["sorted"].apply(
        lambda x: conditions_dict[x]
    )
    conditions["l_conditions"] = conditions["conditions"].apply(lambda x: [x])

    return conditions


def most_common(lst):
    return max(set(lst), key=lst.count)


def create_conditions_table(conditions: pd.DataFrame) -> pd.DataFrame:
    conditions_table = pd.DataFrame(
        conditions.groupby("condition_id")["l_conditions"].apply(sum).apply(most_common)
    )
    conditions_table = conditions_table.set_axis(["name"], axis=1, inplace=False)
    conditions_table = conditions_table.rename_axis(["id"], axis=0)

    return conditions_table


def create_study_conditions_table(conditions: pd.DataFrame) -> pd.DataFrame:
    study_conditions = (
        conditions[["study_id", "condition_id"]]
        .rename(columns={"study_id": "study", "condition_id": "condition"})
        .reset_index(drop=True)
    )

    return study_conditions


def add_study_id(table: pd.DataFrame, connection) -> pd.DataFrame:
    db = create_engine(DATABASE_URL)
    study_ids = pd.read_sql("select id, nct_id from studies", connection)
    merged_table = table.merge(study_ids, left_on="study", right_on="nct_id")

    return merged_table[["id", "study", "condition"]]


def upload_to_db(table_name: str, table: pd.DataFrame, connection):
    table.to_sql(str, connection, index=False, if_exists="append")


# requires studies_workflow to write pre_cleaned studies_table to disk
def conditions_workflow(connection) -> None:
    studies_table = load_pre_cleaned_studies_table()

    conditions = get_conditions(studies_table=studies_table)
    conditions_table = create_conditions_table(conditions=conditions)
    upload_to_db("conditions", conditions_table, connection)

    study_conditions_table = create_study_conditions_table(conditions=conditions)
    study_conditions_table = add_study_id(study_conditions_table, connection)
    upload_to_db("study_conditions", study_conditions_table, connection)

    print(conditions_table)
    print(conditions_table.keys())
    print(conditions_table.iloc[1])

    print(study_conditions_table)
    print(study_conditions_table.keys())
    print(study_conditions_table.iloc[1])


if __name__ == "__main__":
    connection = create_engine(DATABASE_URL).connect()
    conditions_workflow(connection)
