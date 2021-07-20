from app.treatments import bp
from app.treatments.controllers import treatments


@bp.route('/')
def main():
	return "Hello World	"


@bp.route('/treatment/<string:name>/demographics')
def get_treatment_demographics(name):
	baselines = treatments.get_demographics(name)
	return {'baselines': [x.to_dict() for x in baselines]}


@bp.route('/treatment/<string:name>/effects')
def get_treatment_effects(name):
	effects = treatments.get_effects(name)
	return {'effects': [x.to_dict() for x in effects]}
	