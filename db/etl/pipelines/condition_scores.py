import os
import sqlalchemy as sa
from sqlalchemy import text
from pipelines.pipeline import Pipeline

from pyspark.sql import SparkSession
from configparser import ConfigParser


class ConditionScoresPipeline(Pipeline):
	def run(self):

		session = SparkSession(self.context)

		db_conf = ConfigParser()
		db_conf.read('../db_properties.ini')
		db_url = db_conf['postgres']['url']
		db_props = {
			'username': db_conf['postgres']['user'],
			'password': db_conf['postgres']['password'],
			'driver': db_conf['postgres']['driver']
		}

		table = '(select g.study as study, g.id as group_id, title,\
	       administrations.id as admin_id,\
	       name, t.id as treat_id,\
	       c.id as comp_id, p_value,\
	       a.from_study, method, a.id as analytic_id\
	       from (administrations\
			    join groups g on g.id = administrations."group"\
				join comparison c on g.id = c."group"\
			    join analytics a on c."analytic"=a.id\
			    join treatments t on administrations.treatment = t.id)\
			where a.p_value is not NULL) foo'

		analytics_base = session.read.jdbc(url=db_url, table=table, properties=db_props)

		null_treatment_id = 2182
		no_treat_groups = analytics_base.filter(f'treat_id = {null_treatment_id}').select('group_id').drop_duplicates()
		one_treat_groups = analytics_base.select(['group_id', 'treat_id'])\
			.drop_duplicates()\
			.groupBy('group_id')\
			.count()\
			.filter('count<2')\
			.select('group_id')

		target_groups = one_treat_groups.union(no_treat_groups).drop_duplicates()

		two_group_analytics = analytics_base.select('group_id', 'analytic_id')\
			.drop_duplicates()\
			.groupBy('analytic_id')\
			.count()\
			.select('analytic_id')

		single_analytics = analytics_base.select('p_value', 'analytic_id', 'group_id', 'study', 'treat_id', 'name')\
			.join(two_group_analytics, 'analytic_id')\
			.join(target_groups, 'group_id')\
			.filter(f'treat_id!={null_treatment_id}')\
			.drop_duplicates()

		study_conditions_table = '(select studies.id as study, c.name as condition, c.id as cond_id from studies\
			join study_conditions sc on studies.id = sc.study\
			join conditions c on sc.condition = c.id) bar';
		study_conditions = session.read.jdbc(url=db_url, table=study_conditions_table, properties=db_props)
		single_analytic_conditions = single_analytics.join(study_conditions, 'study')
		singular_treat_scores = single_analytic_conditions.groupBy('treat_id', 'cond_id').mean('p_value')\
			.withColumnRenamed('avg(p_value)', 'singular_score')

		mixed_scores = analytics_base.select('study','p_value', 'analytic_id', 'treat_id')\
			.join(study_conditions, 'study')\
			.drop_duplicates()\
			.select('cond_id', 'treat_id', 'p_value')\
			.groupBy('cond_id', 'treat_id').mean('p_value')\
			.withColumnRenamed('avg(p_value)', 'mixed_score')

		mixed_and_singular = mixed_scores.join(
			singular_treat_scores, 
			['cond_id', 'treat_id'],
			'full').withColumnRenamed('cond_id', 'condition')\
			.withColumnRenamed('treat_id', 'treatment')

		# Clear existing table
		db_engine = sa.create_engine('postgresql://meditreats:meditreats@localhost:5432/meditreats')
		db_connection = db_engine.connect()
		result = db_connection.execute(text('TRUNCATE TABLE conditionscores'))
		result.close()


		mixed_and_singular.write.jdbc(
			url=db_url, 
			table='conditionscores',
			mode='append',
			properties=db_props)
