import os
import pickle
import pandas as pd

from sqlalchemy import create_engine
from tqdm import tqdm


DATA_PATH = os.environ.get("DATA_PATH", default="/Users/porterhunley/datasets")
DATABASE_URL = os.environ.get("DATABASE_URL", default="postgresql://davonprewitt@localhost:5432")

def get_outcome_and_intervention_modules(studies):
    outcome_modules = []
    intervention_modules = []

    outcome_study_ids = []
    arm_study_ids = []
    for study in studies:
        if (
            "ResultsSection" in study["Study"]
            and "OutcomeMeasuresModule" in study["Study"]["ResultsSection"]
        ):
            outcome_modules.append(study["Study"]["ResultsSection"]["OutcomeMeasuresModule"])
            outcome_study_ids.append(study['Study']['ProtocolSection']['IdentificationModule']['NCTId'])

        elif "ArmsInterventionsModule" in study["Study"]["ProtocolSection"]:
            intervention_modules.append(study["Study"]["ProtocolSection"]["ArmsInterventionsModule"])
            arm_study_ids.append(study['Study']['ProtocolSection']['IdentificationModule']['NCTId'])

    return outcome_modules, outcome_study_ids, intervention_modules, arm_study_ids 


def create_outcomes_table_helper(studies) -> pd.DataFrame:
    outcome_modules, outcome_study_ids, intervention_modules, arm_study_ids = get_outcome_and_intervention_modules(studies)
    group_df = {
        "study_id": [],
        "group_id": [],
        "title": [],
        "description": [],
    }

    for i, module in enumerate(outcome_modules):
        for measure in module["OutcomeMeasureList"]["OutcomeMeasure"]:
            try:
                for admin in measure.get("OutcomeGroupList", {"OutcomeGroup": []})[
                    "OutcomeGroup"
                ]:
                    group_df["study_id"].append(outcome_study_ids[i])
                    group_df["group_id"].append(admin.get("OutcomeGroupId", "NA"))
                    group_df["title"].append(admin.get("OutcomeGroupTitle", "NA"))
                    group_df["description"].append(
                        admin.get("OutcomeGroupDescription", "NA")
                    )
            except KeyError as e:
                continue

    #For studies without results
    for i, module in enumerate(intervention_modules):
        try:
            for group in module.get("ArmGroupList", {"ArmGroup": []})["ArmGroup"]:
                group_df["study_id"].append(arm_study_ids[i])
                group_df["group_id"].append("NA")
                group_df["title"].append(group.get("ArmGroupLabel", "NA"))
                group_df["description"].append(group.get("ArmGroupDescription", "NA"))
        except KeyError as e:
            print(e)
            continue

    groups_table_df = pd.DataFrame.from_dict(group_df).reset_index(drop=True)
    return groups_table_df


def add_study_id(table: pd.DataFrame, connection) -> pd.DataFrame:
    study_ids = pd.read_sql("select id as std_id, nct_id from temp_schema.studies", connection)
    merged_table = table.merge(study_ids, left_on="study", right_on="nct_id")\
        .drop(columns=['study'], axis=1)\
        .rename(columns={ 'std_id': 'study' })

    return merged_table[["id", "study", "title", "study_id", "description"]]


# this takes in initial studies parsing
def create_groups_table():
    groups_table_dfs = []
    directory = DATA_PATH + "/clinical_trials/"
    print("Deserializing studies")
    for studies_data_pickle_file in tqdm(os.listdir(directory)):
        studies_file = os.path.join(directory, studies_data_pickle_file)
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
    studies_table.to_sql("groups", connection, index=False, if_exists="append", schema='temp_schema')


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
