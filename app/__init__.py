import pinecone
import graphene
import stripe
import openai
import boto3

from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_graphql import GraphQLView


db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
cognito_client = boto3.client('cognito-idp')

gpt_vectors = pinecone.Index('gpt')

def create_app(config_file=None):
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_pyfile(config_file)


	from app.schema import Query
	schema = graphene.Schema(query=Query)
	app.add_url_rule(
		'/graphql-api',
		view_func=GraphQLView.as_view(
				'graphql',
				schema=schema,
				graphiql=True))

	initialize_extensions(app)
	register_blueprints(app)

	return app


def initialize_extensions(app):
	from app.extensions import IntListConverter

	openai.organization = "org-j6fGVx3OgjgpAbCQFHOmdEUe"
	openai.api_key = app.config['OPENAI_API_KEY']
	stripe.api_key = app.config['STRIPE_SECRET_KEY']
	pinecone.init(api_key = app.config['PINECONE_API_KEY'], environment="us-west1-gcp")

	cognito_client = boto3.client('cognito-idp',
		aws_access_key_id=app.config['AWS_ACCESS_KEY'],
		aws_secret_access_key=app.config['AWS_SECRET_KEY'],
		aws_session_token=app.config['AWS_SESSION_TOKEN'])

	db.init_app(app)
	migrate.init_app(app, db)
	cors.init_app(app, support_credentials=True)
	app.url_map.converters['int_list'] = IntListConverter


def register_blueprints(app):
	from app.treatments import bp as treatments_bp
	from app.studies import bp as studies_bp
	from app.conditions import bp as conditions_bp
	from app.blogs import bp as blogs_bp
	from app.feedback import bp as feedback_bp
	from app.measures import bp as measures_bp 
	from app.users import bp as users_bp 

	app.register_blueprint(treatments_bp, url_prefix='/treatments')
	app.register_blueprint(studies_bp, url_prefix='/studies')
	app.register_blueprint(conditions_bp, url_prefix='/conditions')
	app.register_blueprint(blogs_bp, url_prefix='/blogs')
	app.register_blueprint(feedback_bp, url_prefix='/feedback')
	app.register_blueprint(measures_bp, url_prefix='/measures')
	app.register_blueprint(users_bp, url_prefix='/users')
