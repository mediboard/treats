from app.conditions import bp
from app.conditions import controller
from flask_cors import cross_origin
import app.conditions.controller as controller


@bp.route('/')
@cross_origin(supports_credentials=True)
def main():
	return "Hello Conditions"


@bp.route('/<string:condition_name>')
@cross_origin(supports_credentials=True)
def get_condition(condition_name):
	condition, count = controller.get_condition(condition_name)

	return {'condition': {**condition.to_dict(), 'no_studies': count}}


@bp.route('/<string:condition_name>/demographics')
@cross_origin(supports_credentials=True)
def get_demographics(condition_name):
	demos = controller.get_demographics(condition_name)

	return {'demographics': [{'sub_type': subtype.value, 'value':value} for subtype, value in demos]}
