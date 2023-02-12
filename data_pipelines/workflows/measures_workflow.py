"""writes measures table"""
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
    for study in studies:
        if (
            "ResultsSection" in study["Study"]
            and "OutcomeMeasuresModule" in study["Study"]["ResultsSection"]
        ):
            outcome_modules.append(
                study["Study"]["ResultsSection"]["OutcomeMeasuresModule"]
            )
            continue
        elif "ArmsInterventionsModule" in study["Study"]["ProtocolSection"]:
            intervention_modules.append(
                study["Study"]["ProtocolSection"]["ArmsInterventionsModule"]
            )
            continue

        identification_module = study["Study"]["ProtocolSection"][
            "IdentificationModule"
        ]
        if "OfficialTitle" in identification_module:
            study_title = identification_module["OfficialTitle"]
        else:
            study_title = identification_module["BriefTitle"]

    return outcome_modules, intervention_modules


def create_measurements_table_helper(studies):
    outcome_modules, intervention_modules = get_outcome_and_intervention_modules(
        studies
    )
    df = {
        "study_id": [],
        "measure": [],
        "type": [],
        "description": [],
        "dispersion_param": [],
        "measure_param": [],
        "units": [],
    }

    for i, module in enumerate(outcome_modules):
        study_id = studies[i]["Study"]["ProtocolSection"]["IdentificationModule"][
            "NCTId"
        ]
        for measure in module["OutcomeMeasureList"]["OutcomeMeasure"]:
            df["type"].append(measure.get("OutcomeMeasureType", "NA"))
            df["measure"].append(measure.get("OutcomeMeasureTitle", "NA"))
            df["description"].append(measure.get("OutcomeMeasureDescription", "NA"))
            df["measure_param"].append(measure.get("OutcomeMeasureParamType", "NA"))
            df["dispersion_param"].append(measure.get("OutcomeMeasureDispersionType", "NA"))
            df["units"].append(measure.get("OutcomeMeasureUnitOfMeasure", "NA"))
            df["study_id"].append(study_id)

    for i, module in enumerate(intervention_modules):
        study_id = studies[i]["Study"]["ProtocolSection"]["IdentificationModule"][
            "NCTId"
        ]
        for measure in module.get("ArmGroupList", {"ArmGroup": []})["ArmGroup"]:
            # Measure data is unstructured and often has other fields in the description.
            df["type"].append("NA")
            df["measure"].append(measure.get("ArmGroupLabel", "NA"))
            df["description"].append(measure.get("ArmGroupDescription", "NA"))
            df["measure_param"].append("NA")
            df["dispersion_param"].append("NA")
            df["units"].append("NA")
            df["study_id"].append(study_id)
    return pd.DataFrame.from_dict(df).reset_index(drop=True)


def create_measurements_table():
    measurements_table_dfs = []
    directory = DATA_PATH + "/clinical_trials/"
    print("Deserializing studies...")
    for studies_data_pickle_file in tqdm(os.listdir(directory)):
        studies_file = os.path.join(directory, studies_data_pickle_file)
        with open(studies_file, "rb") as f:
            studies_data = pickle.load(f)
            measurements_table_df = create_measurements_table_helper(
                studies=studies_data
            )
            measurements_table_dfs.append(measurements_table_df)

    measurements_table = pd.concat(measurements_table_dfs).reset_index(drop=True)
    return measurements_table


def clean_measures_table(measures_table: pd.DataFrame) -> pd.DataFrame:
    db_measures_table = measures_table.rename(
        columns={
            "study_id": "study",
            "measure": "title",
            "dispersion_param": "dispersion",
            "measure_param": "param",
        }
    ).rename_axis(["id"], axis=0)

    dispersion_map = {
        "Standard Deviation": "STANDARD_DEVIATION",
        "95% Confidence Interval": "CONFIDENCE_INTERVAL_95",
        "Standard Error": "STANDARD_ERROR",
        "Full Range": "FULL_RANGE",
        "Geometric Coefficient of Variation": "GEOMETRIC_COEFFICIENT_OF_VARIATION",
        "Inter-Quartile Range": "INTER_QUARTILE_RANGE",
        "90% Confidence Interval": "CONFIDENCE_INTERVAL_90",
        "80% Confidence Interval": "CONFIDENCE_INTERVAL_80",
        "97% Confidence Interval": "CONFIDENCE_INTERVAL_97",
        "99% Confidence Interval": "CONFIDENCE_INTERVAL_99",
        "60% Confidence Interval": "CONFIDENCE_INTERVAL_60",
        "96% Confidence Interval": "CONFIDENCE_INTERVAL_96",
        "98% Confidence Interval": "CONFIDENCE_INTERVAL_98",
        "70% Confidence Interval": "CONFIDENCE_INTERVAL_70",
        "85% Confidence Interval": "CONFIDENCE_INTERVAL_85",
        "75% Confidence Interval": "CONFIDENCE_INTERVAL_75",
        "94% Confidence Interval": "CONFIDENCE_INTERVAL_94",
        "100% Confidence Interval": "CONFIDENCE_INTERVAL_100",
        "68% Confidence Interval": "CONFIDENCE_INTERVAL_68",
        "NA": "NA",
    }

    db_measures_table["dispersion"] = (
        db_measures_table["dispersion"]
        .apply(lambda x: x if "." not in x else x[: x.index(".")] + x[x.index("%") :])
        .apply(lambda x: dispersion_map[x])
    )

    db_measures_table["param"] = (
        db_measures_table["param"].str.upper().str.replace(" ", "_")
    )

    measure_type_map = {
        "Primary": "PRIMARY",
        "Secondary": "SECONDARY",
        "Other Pre-specified": "OTHER",
        "Post-Hoc": "OTHER",
        "NA": "OTHER",
    }

    db_measures_table["type"] = db_measures_table["type"].apply(
        lambda x: measure_type_map[x]
    )

    db_measures_table = db_measures_table[
        ["study", "title", "description", "dispersion", "type", "param", "units"]
    ]

    db_measures_table["description"].str.len().max()

    return db_measures_table


def upload_to_db(measures_table: pd.DataFrame, connection):
    measures_table.to_sql("measures", connection, index=False, if_exists="append", schema='temp_schema')


def add_study_id(table: pd.DataFrame, connection) -> pd.DataFrame:
    study_ids = pd.read_sql("select id as std_id, nct_id from temp_schema.studies", connection)
    merged_table = table.merge(study_ids, left_on="study", right_on="nct_id")\
        .drop(columns=['study', 'nct_id'], axis=1)\
        .rename(columns={ 'std_id': 'study' })

    return merged_table


# requires studies_workflow pulling down raw studies to disk
def measures_workflow(connection) -> None:
    measures_table = create_measurements_table()
    db_measures_table = clean_measures_table(measures_table=measures_table)
    db_measures_table = add_study_id(db_measures_table, connection)
    upload_to_db(db_measures_table, connection)

    # used by outcomes workflow
    db_measures_table.to_pickle(DATA_PATH + "/measures_table.pkl")

    print(db_measures_table)
    print(db_measures_table.keys())
    print(db_measures_table.iloc[1])


if __name__ == "__main__":
    connection = create_engine(DATABASE_URL).connect()
    measures_workflow(connection)
