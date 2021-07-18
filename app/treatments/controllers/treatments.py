from app.treatments.models import Baseline, Treatment, Administration
from app import db


def get_demographics(treatment_name):
	baselines = Treatment.query.filter_by(name=treatment_name).join(Administration).all()
	print(baselines)
	return baselines

