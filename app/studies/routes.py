from app.studies import bp
from flask_cors import cross_origin
from app.studies import controller


@bp.route('/')
@cross_origin(supports_credentials=True)
def main():
	return "Hello Studies"


@bp.route('/<string:study_id>')
@cross_origin(supports_credentials=True)
def get_study(study_id):
	studies = controller.get_study(study_id)
	return {'studies': [study.to_dict() for study in studies]}

