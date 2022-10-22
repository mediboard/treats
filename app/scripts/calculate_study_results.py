from sqlalchemy import create_engine, func, bindparam
from sqlalchemy.schema import Table, MetaData, Column
from sqlalchemy.sql import select, insert, distinct, update, join
from sqlalchemy.types import String, Integer, Float, Numeric


DATABASE_URL = 'postgresql://meditreats:meditreats@df-treats-db.cs6hxh6ocizm.us-west-2.rds.amazonaws.com:5432'

def calculate_results_summary(mean, mn):
    if (mn and mn <= .15):
        return 10 if mean <= .15 else 8 

    return 0

if __name__ == '__main__':
	studies_table = Table(
	    "studies", MetaData(),
	    Column('id', String(11), primary_key=True),
		Column('results_summary', Integer()))

	analytics_table = Table(
	    "analytics", MetaData(),
	    Column('id', Integer(), primary_key=True),
	    Column('p_value', Float()),
	    Column('study', String(11)))

	# Query of studies and their analytics
	# Calculate the summary
	# Put it back in
	engine = create_engine(DATABASE_URL)

	conn = engine.connect()

	j = studies_table.join(analytics_table, analytics_table.c.study == studies_table.c.id)
	select_smt = select(studies_table, func.avg(analytics_table.c.p_value), func.min(analytics_table.c.p_value))\
		.select_from(j)\
		.group_by(studies_table.c.id)

	values = []
	for (i, row) in enumerate(conn.execute(select_smt)):
		study_id = row[0]
		avg = row[2]
		mn = row[3]

		values.append({
			'study_id': study_id,
			'results_summary': calculate_results_summary(avg, mn)
		})

	print(values[0:10])
	print(len(values))

	# update_stmt = update(studies_table)\
	# 	.where(studies_table.c.id == bindparam('study_id'))\
	# 	.values(results_summary=bindparam('results_summary'))

	# conn.execute(update_stmt, values)


