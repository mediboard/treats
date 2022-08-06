import os
import pickle
import typing
import pandas as pd


# TODO update this
STUDIES_PICKLE_FILE_PATH = "/Users/pauldittamo/src/mediboard/"


def get_outcome_modules(studies):
    outcome_modules = []
    for study in studies:
        if 'OutcomeMeasuresModule' in study['Study']['ResultsSection']:
            outcome_modules.append(study['Study']['ResultsSection']['OutcomeMeasuresModule'])
            continue
        print('No Results: ', study['Study']['ProtocolSection']['IdentificationModule']['OfficialTitle'])

    return outcome_modules


def create_analytics_table_helper(studies: typing.List[dict]):
    outcome_modules = get_outcome_modules(studies)
    df = {
        'study_id': [],
        'measure': [],
        'groups': [],
        'description': [],  # may or may not be the outcome title
        'method': [],
        'param_type': [],
        'fromStudy': [],
        'pval': [],
        'group_titles': [],
        'is_non_inferiority': [],
        'non_inferiority_type': [],
        'non_inferiority_comment': [],
        'param_value': [],
        'ci_pct': [],
        'ci_lower': [],
        'ci_upper': [],
    }

    for i, module in enumerate(outcome_modules):
        study_id = studies[i]['Study']['ProtocolSection']['IdentificationModule']['NCTId']
        for measure in module['OutcomeMeasureList']['OutcomeMeasure']:
            group_to_title = {}
            for group in measure.get('OutcomeGroupList', {'OutcomeGroup': []})['OutcomeGroup']:
                if group['OutcomeGroupId'] not in group_to_title:
                    group_to_title[group['OutcomeGroupId']] = 'NA'
                group_to_title[group['OutcomeGroupId']] = group.get('OutcomeGroupTitle', 'NA')

            measure_title = measure.get('OutcomeMeasureTitle', 'NA')
            for stat in measure.get('OutcomeAnalysisList', {'OutcomeAnalysis': []})['OutcomeAnalysis']:
                df['study_id'].append(study_id)
                df['measure'].append(measure_title)
                df['groups'].append(stat.get('OutcomeAnalysisGroupIdList', {'OutcomeAnalysisGroupId': []})['OutcomeAnalysisGroupId'])
                df['description'].append(stat.get('OutcomeAnalysisGroupDescription', 'NA'))
                df['method'].append(stat.get('OutcomeAnalysisStatisticalMethod', 'NA'))
                df['param_type'].append(stat.get('OutcomeAnalysisParamType', 'NA'))
                df['fromStudy'].append(True)
                df['pval'].append(stat.get('OutcomeAnalysisPValue', 'NA'))
                df['group_titles'].append(dict([(g, group_to_title.get(g, 'NA')) for g in stat.get('OutcomeAnalysisGroupIdList', {'OutcomeAnalysisGroupId': []})
                                                    ['OutcomeAnalysisGroupId']]))
                df['is_non_inferiority'].append(stat.get('OutcomeAnalysisNonInferiorityType', 'NA'))
                df['non_inferiority_type'].append(stat.get('OutcomeAnalysisNonInferiorityType', 'NA'))
                df['non_inferiority_comment'].append(stat.get('OutcomeAnalysisNonInferiorityComment', 'NA'))
                df['param_value'].append(stat.get('OutcomeAnalysisParamValue', 'NA'))
                df['ci_pct'].append(stat.get('OutcomeAnalysisCIPctValue', 'NA'))
                df['ci_lower'].append(stat.get('OutcomeAnalysisCILowerLimit', 'NA'))
                df['ci_upper'].append(stat.get('OutcomeAnalysisCIUpperLimit', 'NA'))

    return pd.DataFrame.from_dict(df).reset_index(drop=True)


# this takes in initial studies parsing
def create_analytics_table():
    analytics_table_dfs = []
    directory = STUDIES_PICKLE_FILE_PATH + 'clinical_trials/'
    for studies_data_pickle_file in os.listdir(directory):
        studies_file = os.path.join(directory, studies_data_pickle_file)
        print(f"Deserializing {studies_file}")
        with open(studies_file, 'rb') as f:
            studies_data = pickle.load(f)
            analytics_table_df = create_analytics_table_helper(studies=studies_data)
            analytics_table_dfs.append(analytics_table_df)

    analytics_table = pd.concat(analytics_table_dfs).reset_index(drop=True)
    return analytics_table


# requires outcomes table
def analytics_workflow() -> None:
    # maps to non_study_analytics
    analytics_table = create_analytics_table()
    # create_non_study_analytics()
    print(analytics_table)
    print(analytics_table.keys())
    print(analytics_table.iloc[1])
    print(analytics_table[analytics_table['study_id'] == 'NCT03264157'].iloc[1])


if __name__ == "__main__":
    analytics_workflow()
