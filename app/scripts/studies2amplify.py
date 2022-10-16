from sqlalchemy import create_engine
from sqlalchemy.schema import Table, MetaData, Column
from sqlalchemy.sql import select
from sqlalchemy.types import String
import boto3
import boto3.session
from botocore.config import Config
import datetime


DATABASE_URL = 'postgresql://meditreats:meditreats@df-treats-db.cs6hxh6ocizm.us-west-2.rds.amazonaws.com:5432'

if (__name__ == '__main__'):
	engine = create_engine(DATABASE_URL)

	conn = engine.connect()

	studies = Table(
	    "studies", MetaData(),
	    Column('id', String(11), primary_key=True))
	

	dynamodb = boto3.resource('dynamodb',
	                             aws_access_key_id='AKIASGJN6HRUAXIFCVE5',
	                             region_name='us-west-2',
	                             aws_secret_access_key='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')

	table = dynamodb.Table('Study-ohljraujtzh6pk4pnmrbu67qda-staging')

	for (i, row) in enumerate(conn.execute(select(studies))):

		if (i >= 938):
			break	

		table.put_item(
		   Item={
		        'nctId': row[0],
		        'updatedAt': datetime.datetime.now().isoformat()+'Z',
		        'createdAt': datetime.datetime.now().isoformat()+'Z',
		        'noUpvotes': 0,
		        'noUpvotesType': 'upvote',
		        '_version': 1,
		        '_lastChangedAt': int(datetime.datetime.now().timestamp())
		    }
		)

