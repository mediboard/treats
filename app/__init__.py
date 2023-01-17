import graphene
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_graphql import GraphQLView


db = SQLAlchemy()
migrate = Migrate()
cors = CORS()

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

	app.register_blueprint(treatments_bp, url_prefix='/treatments')
	app.register_blueprint(studies_bp, url_prefix='/studies')
	app.register_blueprint(conditions_bp, url_prefix='/conditions')
	app.register_blueprint(blogs_bp, url_prefix='/blogs')
	app.register_blueprint(feedback_bp, url_prefix='/feedback')
