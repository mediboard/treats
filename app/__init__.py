from flask import Flask 

def create_app(config_file=None):
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_pyfile(config_file)
	register_blueprints(app)
	return app

def register_blueprints(app):
	from app.treatments import bp as treatments_bp
	app.register_blueprint(treatments_bp)
	