from app import db
from app.models import Condition, StudyCondition, Baseline, baseline_type, \
	Treatment, StudyTreatment, Analytics, Measure, measure_type, Study, MeasureGroup, MeasureGroupMeasure, \
	ConditionGroup
from sqlalchemy.orm import joinedload, raiseload, contains_eager
from sqlalchemy import func, desc, distinct, asc
from app.utils import calculate_results_summary


ROWS_PER_PAGE=8

def search(query, limit=5):
	processedQuery = query.replace(' ', ' & ') if query[-1] != ' ' else query
	conditions_counts = db.session.query(Condition)\
		.filter(func.lower(Condition.name).match(processedQuery) | func.lower(Condition.name).like(f'%{processedQuery}%'))\
		.limit(limit)\

	return conditions_counts.all()


def get_top_conditions():
	# Manually filtering out Healthy for now
	top_conditions = ['Depression', 'Anxiety', 'Asthma', 'Alcohol Dependence', 'Menopause', 'Insomnia', 'Obesity']
	conditions_counts = db.session.query(Condition, func.count(StudyCondition.study).label('no_studies'))\
		.filter(Condition.name.in_(top_conditions))\
		.join(StudyCondition, StudyCondition.condition == Condition.id)\
		.group_by(Condition.id)\
		.order_by(desc('no_studies'))\
		.all()

	return conditions_counts


def get_measure_groups(condition_id):
	groups = db.session.query(MeasureGroup)\
		.filter(MeasureGroup.condition == condition_id)\
		.all()

	return groups


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
	treatments = db.session.query(Treatment, func.count(distinct(StudyTreatment.study)).label('no_studies'))\
		.join(StudyTreatment, StudyTreatment.treatment == Treatment.id)\
		.join(StudyCondition, StudyCondition.study == StudyTreatment.study)\
		.join(Condition, StudyCondition.condition == Condition.id)\
		.filter(func.lower(Condition.name) == func.lower(name))\
		.group_by(Treatment.id)\
		.order_by(desc(Treatment.no_prescriptions), desc('no_studies'))\
		.all()

	return treatments

def get_treatments_by_condition_group(condition_group):
	treatments = db.session.query(Treatment, func.count(distinct(StudyTreatment.study)).label('no_studies'))\
		.join(StudyTreatment, StudyTreatment.treatment == Treatment.id)\
		.join(StudyCondition, StudyCondition.study == StudyTreatment.study)\
		.join(Condition, StudyCondition.condition == Condition.id)\
		.join(ConditionGroup, ConditionGroup.id == Condition.condition_group)\
		.filter(ConditionGroup.name == condition_group)\
		.group_by(Treatment.id)\
		.order_by(desc('no_studies'))\
		.all()

	return treatments

def get_condition_group(condition_group_title):
	condition_group = db.session.query(ConditionGroup)\
		.join(Condition, Condition.condition_group == ConditionGroup.id)\
		.filter(ConditionGroup.name == condition_group_title)\
		.options(contains_eager(ConditionGroup.conditions))\
		.all()

	return condition_group[0]


def get_no_group_studies(condition_group_title):
	no_studies = db.session.query(func.count(distinct(StudyCondition.id)).label('no_studies'))\
		.join(Condition, Condition.id == StudyCondition.condition)\
		.join(ConditionGroup, ConditionGroup.id == Condition.condition_group)\
		.filter(ConditionGroup.name == condition_group_title)\
		.all()

	return no_studies[0]


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


def get_studies(name, treatment_id, page=1):
	studies = db.session.query(Study, func.avg(Analytics.p_value).label('mean'), func.min(Analytics.p_value).label('min'))\
		.join(StudyCondition, Study.id == StudyCondition.study)\
		.join(StudyTreatment, StudyTreatment.study == Study.id)

	if (treatment_id):
		studies = studies.where(StudyTreatment.treatment == treatment_id)

	studies = studies.join(Condition, Condition.id == StudyCondition.condition)\
		.filter(func.lower(Condition.name) == func.lower(name))\
		.join(Analytics, Analytics.study == Study.id)\
		.join(Measure, Analytics.measure == Measure.id)\
		.filter(Measure.type == measure_type.PRIMARY)\
		.group_by(Study.id)\
		.order_by(asc('min'), asc('mean'))\
		.paginate(page, ROWS_PER_PAGE)

	study_items = studies.items
	study_items.sort(key=lambda x: calculate_results_summary(x[1], x[2]), reverse=True)

	return study_items, studies.next_num, studies.total


def get_no_treatments(name):
	no_treatments = db.session.query(func.count(distinct(Treatment.id)).label('no_treatments'))\
		.join(StudyTreatment, StudyTreatment.treatment == Treatment.id)\
		.join(StudyCondition, StudyCondition.study == StudyTreatment.study)\
		.join(Condition, StudyCondition.condition == Condition.id)\
		.filter(Condition.name == name)\
		.group_by(Condition.name).all()

	return no_treatments


def get_no_studies(name):
	no_studies = db.session.query(func.count(distinct(StudyCondition.study)).label('no_studies'))\
		.join(Condition, Condition.id == StudyCondition.condition)\
		.filter(Condition.name == name)\
		.group_by(Condition.name).all()

	return no_studies
