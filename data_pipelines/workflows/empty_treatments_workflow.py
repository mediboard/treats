import pandas as pd
from sqlalchemy import create_engine, func, bindparam
from sqlalchemy.schema import Table, MetaData, Column
from sqlalchemy.sql import select, insert, distinct, update, join
from sqlalchemy.types import String, Integer, Float, Numeric

treatments_table = Table(
  "treatments", MetaData(),
  Column('id', Integer(), primary_key=True),
  Column('name', String()))


def create_null_treatment(connection):
  ins = treatments_table.insert().values(name='N/A')
  result = connection.execute(ins)

  return result

def empty_treatments_workflow(connection):
  # Create "N/A" treatment
  # Select all the groups with no administrations, then give them "N/A"
  create_null_treatment(connection)

  # groups = pd.read_sql("select * from groups", connection);
  # admins = pd.read_sql("select * from administrations", connection);
  # treatments = pd.read_sql("select * from treatments", connection);


