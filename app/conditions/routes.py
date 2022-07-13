from app.conditions import bp
from app.errors import create_notfound_error
from app.conditions import controller
from flask_cors import cross_origin
import app.conditions.controller as controller
from flask import request


@bp.route('/')
@cross_origin(supports_credentials=True)
def main():
	return "Hello Conditions"


@bp.route('/search')
@cross_origin(supports_credentials=True)
def search():
	query = request.args.get('q')
	limit = request.args.get('limit')
	conditions_counts = controller.search(query, limit or 5)

	
	return {'conditions': [{**x.to_dict(), 'no_studies': y} for x,y in conditions_counts]}


@bp.route('/top')
@cross_origin(supports_credentials=True)
def get_top_conditions():
	top_conditions_counts = controller.get_top_conditions();

	return {'conditions': [{**x.to_dict(), 'no_studies':y} for x,y in top_conditions_counts]}


@bp.route('/<string:condition_name>')
@cross_origin(supports_credentials=True)
def get_condition(condition_name):
	condition_count = controller.get_condition(condition_name)
	if (not condition_count):
		return create_notfound_error('Condition {0} not found'.format(condition_name))

	condition, count = condition_count
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