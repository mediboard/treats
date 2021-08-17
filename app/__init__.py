from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS


db = SQLAlchemy()
migrate = Migrate()
cors = CORS()

def create_app(config_file=None):
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_pyfile(config_file)
	register_blueprints(app)
	initialize_extensions(app)
	return app


def initialize_extensions(app):
	db.init_app(app)
	migrate.init_app(app, db)
	cors.init_app(app, support_credentials=True)


def register_blueprints(app):
	from app.treatments import bp as treatments_bp
	app.register_blueprint(treatments_bp)
