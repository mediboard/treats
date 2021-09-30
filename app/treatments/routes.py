from app.treatments import bp
from app.treatments.controllers import treatments
from app.utils import removekey_oop
from flask_cors import cross_origin


@bp.route('/')
@cross_origin(supports_credentials=True)
def main():
	return "Hello Treatments"


@bp.route('/<string:name>/demographics')
@cross_origin(supports_credentials=True)
def get_treatment_demographics(name):
	baselines = treatments.get_demographics(name)
	return {'baselines': [{'sub_type': subtype.value, 'value':value} for subtype, value in baselines]}


@bp.route('/<string:name>/effects')
@cross_origin(supports_credentials=True)
def get_treatment_effects(name):
	effects = treatments.get_effects(name)
	return {'effects': [{'name':name, 'effected':effected, 'at_risk':at_risk, 'no_studies':count} for name,effected,at_risk,count in effects]}


@bp.route('/<string:name>/conditions')
@cross_origin(supports_credentials=True)
def get_treatment_conditions(name):
	conditions_analytics = treatments.get_conditions(name, True)
	# First get the conditions indexable by id
	id_2_condition = {}
	for condition,analytic in conditions_analytics:
		if condition.id not in id_2_condition:
			id_2_condition[condition.id] = {**condition.to_dict(), 'analytics': []}

		id_2_condition[condition.id]['analytics'].append(analytic.to_small_dict())

	for val in id_2_condition.values():
		val['no_studies'] = len(set([x['study'] for x in val['analytics']]))

	return {'conditions': list(id_2_condition.values())}


@bp.route('/<string:name>/scores')
@cross_origin(supports_credentials=True)
def get_condition_scores(name):
	scores = treatments.get_condition_scoring(name)
	return {'condition_scores': [{**x.to_dict(), 'name':y.name} for x,y in scores]}


@bp.route('/<string:name>/spread')
@cross_origin(supports_credentials=True)
def get_treatment_spreaed(name):
	analytics_and_measures = treatments.get_scoring_spread(name)

	analytics = [x.to_dict() for x in list(set([x for x,y in analytics_and_measures]))]
	measures = [x.to_dict() for x in list(set([y for x,y in analytics_and_measures]))]

	smaller_analytics = [removekey_oop(x, 'non_inferiority_comment') for x in analytics]
	smaller_measures = [{
		'id': x['id'],
		'title': x['title'],
		'type': x['type'],
		'param': x['param'],
		'units': x['units']
	} for x in measures]


	return {'spread': {
		'analytics': smaller_analytics,
		'measures': smaller_measures
	}}
