from app import db
from app.models import Condition, StudyCondition, Baseline, baseline_type
from sqlalchemy import func

def get_condition(name):
	condition = db.session.query(Condition)\
		.filter(func.lower(Condition.name) == func.lower(name))\
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
