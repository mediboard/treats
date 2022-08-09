import os
import pickle
import typing
import pandas as pd

from math import sqrt
from scipy import stats


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


def get_sd(outcome_spread, ranges, value, no_obs):
    try:
        if outcome_spread == 'STANDARD_ERROR':
            return sqrt(no_obs) * float(ranges)  # assuming ranges is one number in this case

        if outcome_spread == 'CONFIDENCE_INTERVAL_95':
            return sqrt(int(no_obs)) * (float(ranges[1]) - float(ranges[0])) / 3.92

        if outcome_spread == 'STANDARD_DEVIATION':
            if isinstance(ranges, tuple):
                return -2
            return float(ranges)

        if outcome_spread == 'INTER_QUARTILE_RANGE':
            return (float(ranges[1]) - float(ranges[0])) / 1.35  # Assuming the distribution is normal

    except ValueError as e:  # A little too catch-all imo, this whole system needs to be reworked
        return -1

    return -1


def get_ranges(row):
    if row.dispersion_param in ['INTER_QUARTILE_RANGE', 'CONFIDENCE_INTERVAL_95']:
        return row.lower, row.upper

    return row.dispersion


def get_pval(row_a, row_b):
    mean1 = float(row_a.value.replace(',', '')) if row_a.value != 'NA' else -1
    ranges1 = get_ranges(row_a)
    nobs1 = int(row_a.participants.replace(',', '')) if row_a.participants != 'NA' else -1

    mean2 = float(row_b.value.replace(',', '')) if row_b.value != 'NA' else -1
    ranges2 = get_ranges(row_b)
    nobs2 = int(row_b.participants.replace(',', '')) if row_b.participants != 'NA' else -1

    if -1 in {mean1, nobs1, mean2, nobs2}:
        return -1

    if nobs1 + nobs2 <= 2:
        return -1

    std2 = get_sd(row_a.dispersion_param, ranges2, mean2, nobs2)
    # should this be row_b ?
    std1 = get_sd(row_a.dispersion_param, ranges1, mean1, nobs1)

    if -2 in {std1, std2}:
        return -1

    if -1 in {std1, std2}:
        return -1

    t_test, p_val = stats.ttest_ind_from_stats(mean1=mean1, std1=std1, nobs1=nobs1, mean2=mean2, std2=std2, nobs2=nobs2)

    return float(p_val)


def create_analytics_outside_studies():
    new_analysis = {
        'study_id': [],
        'measure': [],
        'groups': [],
        'description': [],
        'method': [],
        'param_type': [],
        'fromStudy': [],
        'pval': [],
        'group_titles': []
    }
    with open(STUDIES_PICKLE_FILE_PATH + 'pre_cleaned_outcomes_table.pkl', 'rb') as f:
        outcomes_table = pickle.load(f)

    with open(STUDIES_PICKLE_FILE_PATH + 'measures_table.pkl', 'rb') as f:
        measures_table = pickle.load(f)

    study_ids = list(measures_table['study'].value_counts().keys())
    error_counter = 0
    print(len(study_ids))
    for study_count, study_id in enumerate(study_ids):
        print(len(new_analysis['study_id']))
        print(study_count, study_id)
        measures = measures_table[measures_table['study'] == study_id]
        study_measures = list(measures['title'].value_counts().keys())
        for measure in study_measures:
            study_measures_outcomes = outcomes_table[outcomes_table['measure'] == measure]
            outcome_titles = list(study_measures_outcomes['title'].value_counts().keys())  # Need to fill in the NaNs before
            for outcome_title in outcome_titles:
                outcome_group = study_measures_outcomes[study_measures_outcomes['title'] == outcome_title]
                group_ids = list(outcome_group['group_no'].value_counts().keys())
                for i, group_a in enumerate(group_ids):
                    for j, group_b in enumerate(group_ids):
                        if i <= j:
                            continue
                        row_a = outcome_group[outcome_group['group_no'] == group_a].iloc[0]
                        row_b = outcome_group[outcome_group['group_no'] == group_b].iloc[0]

                        try:
                            pval = get_pval(row_a, row_b)
                        except ValueError as e:
                            print(error_counter)
                            error_counter += 1
                            continue

                        new_analysis['study_id'].append(study_id)
                        # TODO just have measure be ID instead of measure title to not need merge with measures
                        new_analysis['measure'].append(measure)
                        new_analysis['groups'].append([group_a, group_b])
                        new_analysis['description'].append(outcome_title)
                        new_analysis['method'].append('t-test')
                        new_analysis['param_type'].append('?')
                        new_analysis['fromStudy'].append(False)
                        new_analysis['pval'].append(pval)
                        new_analysis['group_titles'].append({group_a: row_a['group_title'], group_b: row_b['group_title']})

    return pd.DataFrame.from_dict(new_analysis)


# requires outcomes table
def analytics_workflow() -> None:
    # maps to non_study_analytics
    # analytics_table = create_analytics_table()

    analytics_table_outside_studies = create_analytics_outside_studies()
    analytics_table_outside_studies.to_pickle(STUDIES_PICKLE_FILE_PATH + 'analytics_table_outside_studies.pkl')

    print(analytics_table_outside_studies)
    # print(analytics_table_outside_studies.keys())
    # print(analytics_table_outside_studies.iloc[1])
    #
    # print(analytics_table_outside_studies[analytics_table_outside_studies['pval'] != -1]['study_id'].value_counts())
    # print(analytics_table_outside_studies[analytics_table_outside_studies['study_id'] == 'NCT02055976'])

    print(analytics_table_outside_studies[analytics_table_outside_studies['measure'] == 'Percent Change From Baseline in Fasting Low Density Lipoprotein-Cholesterol (LDL-C) at Day 85'])

    print(analytics_table_outside_studies[analytics_table_outside_studies['measure'] == 'Percent Change From Baseline in Fasting Low Density Lipoprotein-Cholesterol (LDL-C) at Day 113'])


if __name__ == "__main__":
    analytics_workflow()
