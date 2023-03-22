from scipy.stats import t, f
import re
import os
import pickle
import pandas as pd
import numpy as np
from typing import List
from math import sqrt
import warnings

# suppress runtime warnings

from sqlalchemy import create_engine
from tqdm import tqdm


DATABASE_URL = os.environ.get("DATABASE_URL", default="postgresql://davonprewitt@localhost:5432")

def extract_percent(string):
  pattern = r'^([\d\.]+)% Confidence Interval$'
  match = re.match(pattern, string)
  if match:
    percent = float(match.group(1))
    return percent / 100
  else:
    return None


def get_ranges(row):
  if ('Confidence' in row['dispersion_measure']) or row['dispersion_measure'] == 'Inter-Quartile Range':
    return row.lower, row.upper

  return row['dispersion_measure']


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


def get_grouped_pvalue(outcome_measures):
  # Assume incoming dataframe
  # Normal ANOVA or mixed ANOVA
  # Assume all outcomes are done per-measure
  if (len(outcome_measures) < 2):
    return float('nan') 

  outcome_measures['range'] = outcome_measures.apply(lambda row: get_ranges(row), axis=1)
  outcome_measures['sd'] = outcome_measures.apply(lambda row: get_sd(row['dispersion_measure'], row['range'], row['value'], row['no_participants']), axis=1)

  if (outcome_measures.iloc[0]['title_out'] == 'NA'):
    data_df = pd.concat([
      outcome_measures['id_out'],
      outcome_measures['range'],
      outcome_measures['value'],
      outcome_measures['sd'],
      outcome_measures['no_participants']], axis=1)

    return welch_anova(data_df)

  data_df = pd.concat([
    outcome_measures['id_out'],
    outcome_measures['group'],
    outcome_measures['title_out'],
    outcome_measures['range'],
    outcome_measures['value'],
    outcome_measures['sd'],
    outcome_measures['no_participants']], axis=1)

  return two_way_anova(data_df)


def welch_anova(data_df):
  try:
    # args = [np.asarray(arg, dtype=float) for arg in args]
    k = len(data_df)
    ni = data_df['no_participants'] # np.array([len(arg) for arg in args])
    mi = data_df['value'] # np.array([np.mean(arg) for arg in args])
    vi = data_df['sd']**2 # np.array([np.var(arg,ddof=1) for arg in args])
    wi = ni/vi

    tmp =sum((1-wi/sum(wi))**2 / (ni-1))
    tmp /= (k**2 -1)

    dfbn = k - 1
    dfwn = 1 / (3 * tmp)

    m = sum(mi*wi) / sum(wi)
    FS = sum(wi * (mi - m)**2) /((dfbn) * (1 + 2 * (dfbn - 1) * tmp))

    return f.sf(FS, dfbn, dfwn) # equivalent to stats.f.sf

  except ZeroDivisionError:
    return float('nan')


def two_way_anova(df):
  try:
    # Extract unique factor levels and count the number of levels
    a_levels = df['group'].unique()
    b_levels = df['title_out'].unique()
    
    a = len(a_levels)
    b = len(b_levels)
    
    # Calculate the total number of observations and the grand mean
    N = df['no_participants'].sum()
    grand_mean = (df['value'] * df['no_participants']).sum() / N
    
    # Calculate the Sum of Squares
    SSA, SSB, SSAB, SST = 0, 0, 0, 0
    
    for _, row in df.iterrows():
      A_mean = df.loc[df['group'] == row['group'], 'value'].mean()
      B_mean = df.loc[df['title_out'] == row['title_out'], 'value'].mean()
      
      SSA += row['no_participants'] * (A_mean - grand_mean)**2
      SSB += row['no_participants'] * (B_mean - grand_mean)**2
      SSAB += row['no_participants'] * (row['value'] - A_mean - B_mean + grand_mean)**2
      SST += row['no_participants'] * (row['value'] - grand_mean)**2

    SSE = SST - SSA - SSB - SSAB
    
    # Calculate the degrees of freedom
    dfA = a - 1
    dfB = b - 1
    dfAB = (a - 1) * (b - 1)
    dfE = N - a * b
    
    # Calculate the Mean Squares
    MSA = SSA / dfA
    MSB = SSB / dfB
    MSAB = SSAB / dfAB
    MSE = SSE / dfE
    
    # Calculate the F-statistics and p-values
    F_A = MSA / MSE
    F_B = MSB / MSE
    F_AB = MSAB / MSE
    
    p_A = f.sf(F_A, dfA, dfE)
    p_B = f.sf(F_B, dfB, dfE)
    p_AB = f.sf(F_AB, dfAB, dfE)
    
    return p_A

  except ZeroDivisionError:
    return float('nan')


def load_outcome_measures(connection):
  print("Loading outcomes and measures ")
  measures = pd.read_sql("select * from public.measures", connection)
  outcomes = pd.read_sql("select * from public.outcomes where value is not null", connection)

  outcome_measures = outcomes.merge(
    measures,
    left_on=['measure'],
    right_on=['id'],
    suffixes=['_out', '_measure'])

  return outcome_measures


def create_grouped_analytics(outcome_measures):
  # Get p-value per measure
  tqdm.pandas(desc="Getting pvalues...")
  measure_pvals = outcome_measures.groupby('id_measure').progress_apply(get_grouped_pvalue).rename('p_value')

  measures = outcome_measures[['id_measure', 'study_measure']].drop_duplicates()
  measures = measures.merge(measure_pvals, left_on=['id_measure'], right_on=['id_measure'])

  analytics = measures.rename(columns={
    'id_measure': 'measure',
    'study_measure': 'study'
  })

  analytics['method'] = 'ANOVA'

  analytics['id'] = pd.Series(range(1, len(analytics) + 1))

  return analytics 


def upload_to_db(table_name: str, table: pd.DataFrame, connection):
  table.to_sql(table_name, connection, index=False, if_exists="append", schema='public')


def analytics_workflow(connection):
  warnings.filterwarnings("ignore")
  # We're not going to look at the data from the studies because that's too much of a pain
  outcome_measures = load_outcome_measures(connection)

  grouped_analytics = create_grouped_analytics(outcome_measures)

  upload_to_db('analytics', grouped_analytics, connection)


if __name__ == '__main__':
  connection = create_engine(DATABASE_URL).connect()
  analytics_workflow(connection)

