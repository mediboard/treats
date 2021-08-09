from pipelines.pipeline import Pipeline

from pyspark.sql import SparkSession
from configparser import ConfigParser
import os


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

		table = '(select * from (administrations join groups g on g.id = administrations."group"\
		    join comparison c on g.id = c."group"\
		    join analytics a on c."analytic"=a.id\
		    join treatments t on administrations.treatment = t.id) where a.p_value is not NULL) foo'

		analytics_base = session.read.jdbc(url=db_url, table=table, properties=db_props)
		analytics_base.show()
