from app.studies import bp
from flask_cors import cross_origin
from app.studies import controller


@bp.route('/')
@cross_origin(supports_credentials=True)
def main():
	return "Hello Studies"


@bp.route('/<string:name>')
@cross_origin(supports_credentials=True)
def get_study(name):
	study = controller.get_study(name)
	return study.to_dict()

