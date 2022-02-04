from app import db
from app.models import Condition, StudyCondition, Baseline, baseline_type, \
	Treatment, StudyTreatment
from sqlalchemy import func

def get_condition(name):
	condition = db.session.query(Condition, func.count(StudyCondition.study))\
		.filter(func.lower(Condition.name) == func.lower(name))\
		.join(StudyCondition, StudyCondition.condition == Condition.id)\
		.group_by(Condition.id)\
		.first()

	return condition


def get_demographics(name):
	demos = db.session.query(Baseline.sub_type, func.sum(Baseline.value))\
		.join(StudyCondition, StudyCondition.study == Baseline.study)\
		.join(Condition, StudyCondition.condition == Condition.id)\
		.filter(func.lower(Condition.name) == func.lower(name))\
		.filter(Baseline.type != baseline_type.OTHER)\
		.group_by(Baseline.sub_type)\
		.all()

	return demos


def get_treatments(name):
	treatments = db.session.query(Treatment, func.count(StudyTreatment.study))\
		.filter(func.lower(Treatment.name) == func.lower(name))\
		.join(StudyTreatment, StudyCondition.treatment == Treatment.id)\
		.group_by(Treatment.id)\
		.all()

	return treatments


def get_analytics(name, request_args):
	treatment_id = 
