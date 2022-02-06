from app.conditions import bp
from app.conditions import controller
from flask_cors import cross_origin
import app.conditions.controller as controller
from flask import request


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


@bp.route('/<string:condition_name>/analytics')
@cross_origin(supports_credentials=True)
def get_analytics(condition_name):
	analytics = controller.get_analytics(condition_name, request.args)

	return {'analytics': [x.to_small_dict() for x in analytics]}


@bp.route('/<string:condition_name>/treatments')
@cross_origin(supports_credentials=True)
def get_treatments(condition_name):
	treatments = controller.get_treatments(condition_name)

	return {'treatments': [{**x.to_dict(), 'no_studies':y} for x,y in treatments]}