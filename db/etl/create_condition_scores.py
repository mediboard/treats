from pyspark.sql import SparkSession
from configparser import ConfigParser

def create_condition_scores(context, conf):
	session = SparkSession.builder.config(conf).appName('condition_score')
	
	db_conf = ConfigParser()
	db_conf.read('db_properties.ini')
	db_props = {
		''
	}
