"""writes measures table"""
import os
import pickle
import pandas as pd
from sqlalchemy import create_engine


DATA_PATH = os.environ.get("DATA_PATH", default="/Users/davonprewitt/data")
DATABASE_URL = os.environ.get(
    "DATABASE_URL", default="postgresql://davonprewitt@localhost:5432"
)


def get_outcome_modules(studies):
    outcome_modules = []
    for study in studies:
        if (
            "ResultsSection" in study["Study"]
            and "OutcomeMeasuresModule" in study["Study"]["ResultsSection"]
        ):
            outcome_modules.append(
                study["Study"]["ResultsSection"]["OutcomeMeasuresModule"]
            )
            continue

        identification_module = study["Study"]["ProtocolSection"][
            "IdentificationModule"
        ]
        if "OfficialTitle" in identification_module:
            study_title = identification_module["OfficialTitle"]
        else:
            study_title = identification_module["BriefTitle"]
        print("No Results: ", study_title)

    return outcome_modules


def create_measurements_table_helper(studies):
    outcome_modules = get_outcome_modules(studies)
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
            df["dispersion_param"].append(
                measure.get("OutcomeMeasureDispersionType", "NA")
            )
            df["units"].append(measure.get("OutcomeMeasureUnitOfMeasure", "NA"))
            df["study_id"].append(study_id)

    return pd.DataFrame.from_dict(df).reset_index(drop=True)


def create_measurements_table():
    measurements_table_dfs = []
    directory = DATA_PATH + "/clinical_trials/"
    for studies_data_pickle_file in os.listdir(directory):
        studies_file = os.path.join(directory, studies_data_pickle_file)
        print(f"Deserializing {studies_file}")
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
    }

    db_measures_table["type"] = db_measures_table["type"].apply(
        lambda x: measure_type_map[x]
    )

    db_measures_table = db_measures_table[
        ["study", "title", "description", "dispersion", "type", "param", "units"]
    ]

    db_measures_table["description"].str.len().max()

    return db_measures_table


def upload_to_db(studies_table: pd.DataFrame):
    db = create_engine(DATABASE_URL)
    studies_table.to_sql("measures", db, index=False, if_exists="append")


# requires studies_workflow pulling down raw studies to disk
def measures_workflow() -> None:
    measures_table = create_measurements_table()
    db_measures_table = clean_measures_table(measures_table=measures_table)
    upload_to_db(db_measures_table)

    # used by outcomes workflow
    db_measures_table.to_pickle(DATA_PATH + "/measures_table.pkl")

    print(db_measures_table)
    print(db_measures_table.keys())
    print(db_measures_table.iloc[1])


if __name__ == "__main__":
    measures_workflow()
