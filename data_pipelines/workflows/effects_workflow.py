"""writes effects and effectsgroups tables"""
import os
import pickle
import pandas as pd
from typing import List


# TODO update this
STUDIES_PICKLE_FILE_PATH = "/Users/pauldittamo/src/mediboard/"


def create_effects_groups_table_helper(studies: List[dict]) -> pd.DataFrame:
    df = {
        'study_id': [],
        'group_id': [],
        'title': [],
        'description': [],  # Serious or other
    }
    for study in studies:
        study_id = study['Study']['ProtocolSection']['IdentificationModule']['NCTId']
        adverse_module = study['Study']['ResultsSection'].get('AdverseEventsModule', {})  # Small risk here
        for group in adverse_module.get('EventGroupList', {'EventGroup': []})['EventGroup']:
            df['study_id'].append(study_id)
            df['group_id'].append(group.get('EventGroupId', 'NA'))
            df['title'].append(group.get('EventGroupTitle', 'NA'))
            df['description'].append(group.get('EventGroupDescription', 'NA'))

    return pd.DataFrame.from_dict(df).reset_index(drop=True)


def create_effects_table_helper(studies: List[dict]) -> pd.DataFrame:
    df = {
        'study_id': [],
        'group_id': [],
        'effect_name': [],
        'type': [],  # Serious or other
        'organ_system': [],
        'assesment': [],
        'no_effected': [],
        'collection_threshold': [],
        'no_at_risk': [],
    }
    for i, study in enumerate(studies):
        study_id = study['Study']['ProtocolSection']['IdentificationModule']['NCTId']
        adverse_module = study['Study']['ResultsSection'].get('AdverseEventsModule', {}) #Small risk here
        for event in adverse_module.get('OtherEventList', {'OtherEvent': []})['OtherEvent']:
            for stat in event.get('OtherEventStatsList', {'OtherEventStats': []})['OtherEventStats']:
                df['study_id'].append(study_id)
                df['group_id'].append(stat.get('OtherEventStatsGroupId', 'NA'))
                df['effect_name'].append(event.get('OtherEventTerm', 'NA'))
                df['type'].append('other')
                df['organ_system'].append(event.get('OtherEventOrganSystem', 'NA'))
                df['assesment'].append(event.get('OtherEventAssessmentType', 'NA'))
                df['no_effected'].append(float(stat.get('OtherEventStatsNumAffected', 0)) or float(stat.get('OtherEventStatsNumEvents', 0)))
                df['collection_threshold'].append(float(adverse_module.get('EventsFrequencyThreshold', -1)))
                df['no_at_risk'].append(int(stat.get('OtherEventStatsNumAtRisk', -1)))
        for event in adverse_module.get('SeriousEventList', {'SeriousEvent': []})['SeriousEvent']:
            for stat in event.get('SeriousEventStatsList', {'SeriousEventStats': []})['SeriousEventStats']:
                df['study_id'].append(study_id)
                df['group_id'].append(stat.get('SeriousEventStatsGroupId', 'NA'))
                df['effect_name'].append(event.get('SeriousEventTerm', 'NA'))
                df['type'].append('serious')
                df['organ_system'].append(event.get('SeriousEventOrganSystem', 'NA'))
                df['assesment'].append(event.get('SeriousEventAssessmentType', 'NA'))
                df['no_effected'].append(float(stat.get('SeriousEventStatsNumAffected', 0)) or float(stat.get('OtherEventStatsNumEvents', 0)))
                df['collection_threshold'].append(float(adverse_module.get('EventsFrequencyThreshold', -1)))
                df['no_at_risk'].append(int(stat.get('SeriousEventStatsNumAtRisk', -1)))

    return pd.DataFrame.from_dict(df).reset_index(drop=True)


def create_effects_tables() -> tuple[pd.DataFrame, pd.DataFrame]:
    effects_groups_table_dfs = []
    effects_table_dfs = []
    directory = STUDIES_PICKLE_FILE_PATH + 'clinical_trials/'
    for studies_data_pickle_file in os.listdir(directory):
        studies_file = os.path.join(directory, studies_data_pickle_file)
        print(f"Deserializing {studies_file}")
        with open(studies_file, 'rb') as f:
            studies_data = pickle.load(f)
            effects_groups_table_df = create_effects_groups_table_helper(studies=studies_data)
            effects_groups_table_dfs.append(effects_groups_table_df)
            effects_table_df = create_effects_table_helper(studies=studies_data)
            effects_table_dfs.append(effects_table_df)

    effects_groups_table = pd.concat(effects_groups_table_dfs).reset_index(drop=True)
    # added this to handle missing id -> group post merge with effects_groups
    effects_groups_table = effects_groups_table.reset_index(level=0).rename(columns={
        'index': 'id',
    })
    effects_table = pd.concat(effects_table_dfs).reset_index(drop=True)
    return effects_groups_table, effects_table


def clean_effects_groups_table(pre_cleaned_effects_groups_table: pd.DataFrame) -> pd.DataFrame:
    effects_groups_table = pre_cleaned_effects_groups_table.rename(columns={
        'study_id': 'study',
        'group_id': 'study_id'
    })[['title', 'description', 'study_id']]
    return effects_groups_table.rename_axis(['id'], axis=0)


def clean_effects_table(pre_cleaned_effects_table: pd.DataFrame, pre_cleaned_effects_groups_table: pd.DataFrame) -> pd.DataFrame:
    pre_cleaned_effects_groups_table = pre_cleaned_effects_groups_table.drop('title', axis=1)
    pre_cleaned_effects_groups_table = pre_cleaned_effects_groups_table.drop('description', axis=1)
    effects_table = pre_cleaned_effects_table.merge(pre_cleaned_effects_groups_table)
    effects_table = effects_table.rename(columns={
        'id': 'group',
        'study_id': 'study',
        'effect_name': 'name'
    })
    effects_table = effects_table.drop_duplicates(['study', 'group', 'name', 'no_at_risk'])
    effects_table['type'] = effects_table['type'].str.upper()
    effects_table['organ_system'] = effects_table['organ_system'].apply(str)
    effects_table['organ_system'] = effects_table['organ_system'].apply(lambda x: x.split(' (')[0])
    effects_table['organ_system'] = effects_table['organ_system'].str.upper().str.replace(' ', '_').str.replace(',', '')
    effects_table['assesment'] = effects_table['assesment'].str.upper().str.replace(' ', '_').str.replace('-', '_')
    effects_table = effects_table.rename(columns={
        'type': 'effect_type',
        'assesment': 'assessment'
    })
    effects_table = effects_table.drop('group_id', axis=1)
    return effects_table.rename_axis(['id'], axis=0)


# requires studies_workflow pulling down raw studies to disk
def effects_workflow():
    pre_cleaned_effects_groups_table, pre_cleaned_effects_table = create_effects_tables()

    # pre_cleaned effects_groups is used to make effectsadministrations
    pre_cleaned_effects_groups_table.to_pickle(STUDIES_PICKLE_FILE_PATH + 'pre_cleaned_effects_groups_table.pkl')

    effects_groups_table = clean_effects_groups_table(pre_cleaned_effects_groups_table=pre_cleaned_effects_groups_table)
    effects_table = clean_effects_table(pre_cleaned_effects_table=pre_cleaned_effects_table,
                                        pre_cleaned_effects_groups_table=pre_cleaned_effects_groups_table)

    print(effects_groups_table)
    print(effects_groups_table.keys())
    print(effects_groups_table.iloc[1])

    print(effects_table)
    print(effects_table.keys())
    print(effects_table.iloc[1])


if __name__ == "__main__":
    effects_workflow()
