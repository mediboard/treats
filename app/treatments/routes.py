from app.treatments import bp
from app.treatments.controllers import treatments


@bp.route('/')
def main():
	return "Hello World	"


# TODO: these all should have query strings appended to them
@bp.route('/treatment/<string:name>/demographics')
def get_treatment_demographics(name):
	baselines = treatments.get_demographics(name)
	return {'baselines': [x.to_dict() for x in baselines]}


@bp.route('/treatment/<string:name>/effects')
def get_treatment_effects(name):
	effects = treatments.get_effects(name)
	return {'effects': [x.to_dict() for x in effects]}


@bp.route('/treatment/<string:name>/conditions')
def get_treatment_conditions(name):
	conditions_and_counts = treatments.get_conditions_and_counts(name)
	return {'conditions': [{**x.to_dict(), 'no_studies': count} for x,count in conditions_and_counts]}


@bp.route('/treatment/<string:name>/scores')
def get_condition_scores(name):
	scores = treatments.get_condition_scoring(name)
	return {'condition_scores': [x.to_dict() for x in scores]}
	