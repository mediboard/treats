from scipy.stats import t, f
import re

def extract_percent(string):
  pattern = r'^([\d\.]+)% Confidence Interval$'
  match = re.match(pattern, string)
  if match:
    percent = float(match.group(1))
    return percent / 100
  else:
    return None


def get_ranges(row):
  if ('Confidence' in row.dispersion_param) or row.dispersion_param == 'Inter-Quartile Range':
    return row.lower, row.upper

  return row.dispersion


def get_sd(outcome_spread, ranges, value, no_obs):
  try:
    if outcome_spread == 'Standard Error':
      return sqrt(no_obs) * float(ranges)  # assuming ranges is one number in this case

    if 'Confidence' in outcome_spread:
      percent_value = extract_percent(outcome_spread)
      critical_value = t.ppf((1 + percent_value) / 2, no_obs-1)

      return sqrt(int(no_obs)) * ((float(ranges[1]) - float(ranges[0])) / (2*critical_value))

    if outcome_spread == 'Standard Deviation':
      if isinstance(ranges, tuple):
        return -2

      return float(ranges)

    if outcome_spread == 'Inter-Quartile Range':
      return (float(ranges[1]) - float(ranges[0])) / 1.35  # Assuming the distribution is normal

  except ValueError as e:  # A little too catch-all imo, this whole system needs to be reworked
    return -1

  return -1

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


def get_grouped_pvalue(outcome_measures):
  # Assume incoming dataframe
  # Normal ANOVA or mixed ANOVA
  # Assume all outcomes are done per-measure
  ranges = outcome_measures.apply(lambda row: get_ranges(row))
  outcome_measures['sd'] = outcome_measures.apply(lambda row: get_sd(row.outcome_spread, row.range, row.mean, row.nobs))

  if (outcome_measures[0]['title'] == 'NA'):
    data_df = pd.concat([
      outcome_measures['outcome_id'],
      ranges,
      outcome_measures['values'],
      outcome_measures['sd'],
      outcome_measures['participants']], axis=1)

    return welch_anova(data_df, 'outcome_id', 'values', 'sd', 'participants')
    # data_df['pooled'] = data_df['mean'].mean()
    # ssb = (((data_df['mean'] - data_df['pooled']) * 
    #   (data_df['mean'] - data_df['pooled'])) * data_df['nobs']).sum()

    # ssw = ((data_df['nobs'] - 1) * (data_df['sd'] * data_df['sd'])).sum()

    # dfB = len(outcome_measures) - 1
    # dfW = data_df['nobs'].sum() - len(outcome_measures)

    # msB = ssb / dfB
    # msw = ssw / dfW

    # f_stat = msB / msW

    # return 1 - f.cdf(f_stat, dfB, dfW)

  data_df = pd.concat([
    outcome_measures['outcome_id'],
    outcome_measures['group'],
    outcome_measures['title'],
    ranges,
    outcome_measures['values'],
    outcome_measures['sd'],
    outcome_measures['participants']], axis=1)

  return mixed_whelch_anova(data_df, 'title', 'group', 'values', 'sd', 'participants')


def welch_anova(dataframe, group_col, mean_col, sd_col, n_col):
  # Compute the mean and standard error for each group
  group_means = dataframe.groupby(group_col)[mean_col].mean()
  group_sd = dataframe.groupby(group_col)[sd_col].mean()
  group_n = dataframe.groupby(group_col)[n_col].sum()
  group_se = group_sd / group_n**0.5

  # Compute the overall mean and the total degrees of freedom
  overall_mean = dataframe[mean_col].mean()
  total_df = len(dataframe) - 1

  # Compute the sum of squares for the between-group factor
  ss_between = ((group_means - overall_mean)**2 / (group_sd**2 / group_n)).sum()
  df_between = ((group_sd**2 / group_n)**2 / ((group_sd**2 / group_n)**2 / (group_n - 1))).sum()

  # Compute the sum of squares for the within-group factor
  ss_within = ((dataframe[mean_col] - dataframe[group_col].map(group_means))**2).sum()
  df_within = total_df - df_between

  # Compute the Welch's F-statistic and p-value
  f_stat = ss_between / df_between / (ss_within / df_within)
  p_value = 1 - f.cdf(f_stat, df_between, df_within)

  return p_value


def mixed_whelch_anova(dataframe, time_col, group_col, mean_col, sd_col, n_col):
  # Compute the mean and standard error for each time, group combination
  group_means = dataframe.groupby([time_col, group_col])[mean_col].mean().unstack()
  group_sd = dataframe.groupby([time_col, group_col])[sd_col].mean().unstack()
  group_n = dataframe.groupby([time_col, group_col])[n_col].sum().unstack()
  group_se = group_sd / group_n**0.5

  # Compute the overall mean and the total degrees of freedom
  grand_mean = dataframe[mean_col].mean()
  total_df = len(dataframe) - 1

  # Compute the sum of squares for the between-group factor
  ss_between = (group_means.mean() - grand_mean)**2 * np.sum(group_n)

  # Compute the sum of squares for the within-subjects factor
  ss_within = ((group_means - group_means.mean(axis=1, keepdims=True))**2 / group_n * group_se**2).sum().sum()

  # Compute the sum of squares for the interaction effect
  ss_interaction = ((group_means - group_means.mean(axis=1, keepdims=True) - group_means.mean(axis=0, keepdims=True) + grand_mean)**2 / group_n * group_se**2).sum().sum()

  # Compute the degrees of freedom for each factor
  df_between = len(group_means.columns) - 1
  df_within = np.sum(group_n) - len(group_means.columns)
  df_interaction = df_between * df_within

  # Compute the mean squares for each factor
  ms_between = ss_between / df_between
  ms_within = ss_within / df_within
  ms_interaction = ss_interaction / df_interaction

  # Compute the F-statistic and p-value for the between-group factor
  f_stat_between = ms_between / ms_within
  p_value_between = 1 - f.cdf(f_stat_between, df_between, df_within)

  # Compute the F-statistic and p-value for the interaction effect
  f_stat_interaction = ms_interaction / ms_within
  p_value_interaction = 1 - f.cdf(f_stat_interaction, df_interaction, df_within)

  # Combine the p-values for the between-group factor and the interaction effect
  p_value = 1 - (1 - p_value_between) * (1 - p_value_interaction)

  return p_value


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

  study_ids = list(measures_table['study'].value_counts().keys())
  error_counter = 0
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


def analytics_workflow(connection):
  # We're not going to look at the data from the studies because that's too much of a pain
