from app.treatments import bp
from app.treatments.controllers import treatments


@bp.route('/')
def main():
	return "Hello World	"


@bp.route('/treatment/<string:name>/demographics')
def get_treatment_demographics(name):
	baselines = treatments.get_demographics(name)
	return {'baselines': baselines}
	