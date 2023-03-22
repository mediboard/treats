import pandas as pd

from sqlalchemy import create_engine, func, bindparam
from sqlalchemy.schema import Table, MetaData, Column
from sqlalchemy.sql import select, insert, distinct, update, join
from sqlalchemy.types import String, Integer, Float, Numeric, SmallInteger


studies_table = Table(
  "studies", MetaData(),
  Column('id', Integer(), primary_key=True),
  Column('primary_success', SmallInteger()))

def load_analytics_data(connection):
  analytics_data = pd.read_sql("select * from analytics", connection)

  return analytics_data


def load_primary_measures(connection):
  primary_measures = pd.read_sql("select * from measures where type='PRIMARY'", connection)

  return primary_measures


def load_studies(connection):
  studies = pd.read_sql("select * from studies", connection)

  return studies


def upload_to_db(table_name: str, table: pd.DataFrame, connection):
  table.to_sql(table_name, connection, index=False, if_exists="replace", schema='public')


def dataframe_to_dict_list(df):
  dict_list = []
  for index, row in df.iterrows():
    row_dict = {}
    for col in df.columns:
      row_dict['study_' + col] = int(row[col])

    dict_list.append(row_dict)

  return dict_list


def append_to_studies(connection, study_results):
  update_stmt = update(studies_table)\
    .where(studies_table.c.id == bindparam('study_id'))\
    .values(primary_success=bindparam('study_primary_success'))

  connection.execute(update_stmt, dataframe_to_dict_list(study_results))


def map_pvalue(p_value):
  if pd.isna(p_value):
    return -1

  return 1 if p_value <= .05 else 0


def study_success_workflow(connection):
  primary_measures = load_primary_measures(connection)

  analytics = load_analytics_data(connection)

  analytic_measures = analytics.merge(
    primary_measures,
    left_on=['measure'],
    right_on=['id'],
    suffixes=['_analytics', '_measure'])

  study_results = analytic_measures[['study_analytics', 'p_value']].drop_duplicates()

  study_results['primary_success'] = analytic_measures['p_value'].apply(lambda x: 1 if x <= .05 else 0)
  # study_results['primary_success'] = study_results['primary_success'].astype('int8')
  # study_results['study_analytics'] = study_results['study_analytics'].astype('int')

  study_results = study_results.rename(columns={'study_analytics': 'id'}).drop('p_value', axis=1)
  append_to_studies(connection, study_results)

