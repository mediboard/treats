from sqlalchemy import create_engine, func
from sqlalchemy.schema import Table, MetaData, Column
from sqlalchemy.sql import select, insert, distinct
from sqlalchemy.types import String
import datetime


DATABASE_URL = 'postgresql://meditreats:meditreats@df-treats-db.cs6hxh6ocizm.us-west-2.rds.amazonaws.com:5432'

if (__name__ == '__main__'):
	engine = create_engine(DATABASE_URL)

	conn = engine.connect()


	effects = Table(
	    "effects", MetaData(),
	    Column('id', String(11), primary_key=True),
		Column('name', String(100)))

	effects_cluster = Table(
	    "effects_cluster", MetaData(),
	    Column('id', String(11), primary_key=True),
		Column('name', String(100)))

	values = []
	for (i, row) in enumerate(conn.execute(select(distinct(func.lower(effects.c.name))))):
		values.append((i, row[0]))

	conn.execute(insert(effects_cluster).values(values))



