from sqlalchemy import create_engine, func, bindparam, literal_column
from sqlalchemy.schema import Table, MetaData, Column
from sqlalchemy.sql import select, insert, distinct, update, join
from sqlalchemy.types import String, Integer, Float, Numeric


DATABASE_URL = 'postgresql://meditreats:meditreats@df-treats-db.cs6hxh6ocizm.us-west-2.rds.amazonaws.com:5432'


def setup_relevant_tables():
  Table('group_pairs', MetaData(),
    Column('id', Integer(), primary_key=True),
    Column('group_a', Integer(), nullable=True),
    Column('group_b', Integer(), nullable=True))

  Table('treatments', MetaData(),
    Column('id', Integer(), primary_key=True),
    Column('name', String(400)))

  Table('administrations', MetaData(),
    Column('id', Integer(), primary_key=True),
    Column('group', Integer()),
    Column('treatment', Integer()))

  Table('groups', MetaData(),
    Column('id', Integer(), primary_key=True),
    Column('study', String(11)),
    Column('title', String(100)),
    Column('study_id', String(7)))

  Table('measures', MetaData(),
    Column('id', Integer(), primary_key=True),
    Column('study', String(11)),
    Column('title', String(256)))

  Table('studies', MetaData(),
    Column('id', Integer(), primary_key=True))


if __name__ == '__main__':
  group_pairs = Table('group_pairs', MetaData(),
    Column('id', Integer(), primary_key=True),
    Column('group_a', Integer(), nullable=True),
    Column('group_b', Integer(), nullable=True))

  treatments = Table('treatments', MetaData(),
    Column('id', Integer(), primary_key=True),
    Column('name', String(400)))

  administrations = Table('administrations', MetaData(),
    Column('id', Integer(), primary_key=True),
    Column('group', Integer()),
    Column('treatment', Integer()))

  groups = Table('groups', MetaData(),
    Column('id', Integer(), primary_key=True),
    Column('study', String(11)),
    Column('title', String(100)),
    Column('study_id', String(7)))

  measures = Table('measures', MetaData(),
    Column('id', Integer(), primary_key=True),
    Column('study', String(11)),
    Column('title', String(256)))

  studies = Table('studies', MetaData(),
    Column('id', Integer(), primary_key=True))

  engine = create_engine(DATABASE_URL)
  conn = engine.connect()

  select(groups, 
      func.string_agg(treatments.name, literal_column("'%'")).label('treats'))\
    .join(administrations, administrations.c.group == groups.c.id)\
    .join(treatments, treatments.c.id == administrations.treatment)\
    .group_by(groups.c.id)\
    .alias()

  # I think we need dataframes to do these windows
  select(measures, )



  # Calculation strategy
  # For each treatment
  # Find each group (join admin join group)
  # Find each measure (join measure)
  # create diffs in each measure (group_by group, then group by measure)
  # get conditions from measure -> study


