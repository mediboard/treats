import sys
from pipelines.condition_scores import ConditionScoresPipeline

from pyspark import SparkContext, SparkConf


name2pipeline = {}
def register_pipelines(context):
	name2pipeline['condition_scores'] = ConditionScoresPipeline(context)


def run_etl(pipeline_names):
	conf = SparkConf().set("spark.jars", "jars/postgresql-42.2.23.jar")\
		.set('spark.driver.memory', '4g')
	sc = SparkContext("local", "etl", conf=conf)
	register_pipelines(sc)

	for name in pipeline_names:
		name2pipeline[name].run()


if __name__ == '__main__':
	if (len(sys.argv) <= 1):
		print("Not enough arguments")
		exit()

	run_etl(sys.argv[1:])
	print("All pipelines ran successfully")
