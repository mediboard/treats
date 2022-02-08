from app import db
from app.models import Condition, StudyCondition, Baseline, baseline_type, \
	Treatment, StudyTreatment, Analytics, Measure, measure_type
from sqlalchemy import func, desc


def search(query):
	conditions_counts = db.session.query(Condition, func.count(StudyCondition.study).label('no_studies'))\
		.filter(func.lower(Condition.name).match(query) | func.lower(Condition.name).like(f'%{query}%'))\
		.join(StudyCondition, StudyCondition.condition == Condition.id)\
		.group_by(Condition.id)\
		.order_by(desc('no_studies'))\
		.limit(5)\
		.all()

	return conditions_counts


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
	treatments = db.session.query(Treatment, func.count(StudyTreatment.study).label('no_studies'))\
		.join(StudyTreatment, StudyTreatment.treatment == Treatment.id)\
		.join(StudyCondition, StudyCondition.study == StudyTreatment.study)\
		.join(Condition, StudyCondition.condition == Condition.id)\
		.filter(func.lower(Condition.name) == func.lower(name))\
		.group_by(Treatment.id)\
		.order_by(desc('no_studies'))\
		.all()

	return treatments


def get_analytics(name, request_args):
	treatment_id = request_args.get('treatment', '', type=int)

	analytics = db.session.query(Analytics)\
		.join(StudyTreatment, StudyTreatment.study == Analytics.study)

	if (treatment_id != ''):
		analytics = analytics.where(StudyTreatment.treatment == treatment_id)

	analytics = analytics \
		.join(StudyCondition, StudyCondition.study == StudyTreatment.study)\
		.join(Condition, Condition.id == StudyCondition.condition)\
		.filter(func.lower(Condition.name) == func.lower(name))\
		.join(Measure, Analytics.measure == Measure.id)\
		.filter(Measure.type == measure_type.PRIMARY)\
		.all()

	return analytics
