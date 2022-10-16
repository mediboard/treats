from sqlalchemy import create_engine, func, bindparam
from sqlalchemy.schema import Table, MetaData, Column
from sqlalchemy.sql import select, insert, distinct, update
from sqlalchemy.types import String, Integer
import datetime


DATABASE_URL = 'postgresql://meditreats:meditreats@df-treats-db.cs6hxh6ocizm.us-west-2.rds.amazonaws.com:5432'

if (__name__ == '__main__'):
	effect2Cluster = input("Name of effect you want to cluster: ")
	cluster = input("Name of effect cluster you want to put it in: ")

	engine = create_engine(DATABASE_URL)

	conn = engine.connect()

	effects = Table(
	    "effects", MetaData(),
	    Column('id', String(11), primary_key=True),
	    Column('cluster', Integer()),
		Column('name', String(100)))

	effects_cluster = Table(
	    "effects_cluster", MetaData(),
	    Column('id', String(11), primary_key=True),
		Column('name', String(100)))

	effects_stmt = select(effects).where(func.lower(effects.c.name) == effect2Cluster)

	cluster = [x for x in conn.execute(select(effects_cluster).where(effects_cluster.c.name == cluster))][0]

	update_stmt = update(effects)\
						.where(effects.c.id == bindparam('effect_id'))\
						.values(cluster=bindparam('cluster_id'))

	values = []
	for (i, row) in enumerate(conn.execute(effects_stmt)):
		values.append({'effect_id': row[0], 'cluster_id': cluster[0]})

	conn.execute(update_stmt, values)
