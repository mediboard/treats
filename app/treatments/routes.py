from app.treatments import bp
from app.treatments.controllers import treatments
from app.treatments.utils import removekey_oop
from flask_cors import cross_origin


@bp.route('/')
@cross_origin(supports_credentials=True)
def main():
	return "Hello World	"


# TODO: these all should have query strings appended to them
@bp.route('/treatment/<string:name>/demographics')
@cross_origin(supports_credentials=True)
def get_treatment_demographics(name):
	baselines = treatments.get_demographics(name)
	return {'baselines': [{'sub_type': subtype.value, 'value':value} for subtype, value in baselines]}


@bp.route('/treatment/<string:name>/effects')
@cross_origin(supports_credentials=True)
def get_treatment_effects(name):
	effects = treatments.get_effects(name)
	return {'effects': [{'name':name, 'effected':effected, 'at_risk':at_risk, 'no_studies':count} for name,effected,at_risk,count in effects]}


@bp.route('/treatment/<string:name>/conditions')
@cross_origin(supports_credentials=True)
def get_treatment_conditions(name):
	conditions_and_analytics = treatments.get_conditions_and_counts(name, True)
	conditions = [x.to_dict() for x in list(set([x for x,y in conditions_and_analytics]))]
	print(conditions)

	return {'conditions': [{**x.to_dict(), 'no_studies': count} for x,count in conditions_and_counts]}


@bp.route('/treatment/<string:name>/scores')
@cross_origin(supports_credentials=True)
def get_condition_scores(name):
	scores = treatments.get_condition_scoring(name)
	return {'condition_scores': [{**x.to_dict(), 'name':y.name} for x,y in scores]}


@bp.route('/treatment/<string:name>/spread')
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
