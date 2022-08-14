from app.models import Baseline, Treatment, Administration, Study, Group,\
	Effect, EffectGroup, EffectAdministration, Condition, StudyCondition, Comparison, Analytics,\
	ConditionScore, StudyTreatment, Measure
from app.models import baseline_type, measure_type
from app import db
from sqlalchemy.orm import aliased, Bundle
from sqlalchemy import func, distinct, desc
import sqlalchemy as sa


def search_treatments(query, limit=5):
	print(limit)
	processedQuery = query.replace(' ', ' & ') if query[-1] != ' ' else query
	results = db.session.query(Treatment)\
		.filter(Treatment.no_studies > 0)\
		.filter(func.lower(Treatment.name).match(processedQuery) | func.lower(Treatment.name).like(f'%{processedQuery}%'))\
		.order_by(desc(Treatment.no_studies))\
		.limit(limit)\
		.all()

	return results


def get_top_treatments():
	top_treatments = ['Ketamine', 'Gabapentin', 'Pregabalin', 'Citalopram', 'Fluoxetine', 'Estradiol']
	results = db.session.query(Treatment)\
		.filter(Treatment.name.in_(top_treatments))\
		.order_by(desc(Treatment.no_studies))\
		.all()

	return results


def get_demographics(treatment_name):
	treatment_query = db.session.query(Treatment).filter_by(name = treatment_name).subquery()
	admin_query = db.session.query(Administration).join(treatment_query, Administration.treatment == treatment_query.c.id).subquery()
	group_query = db.session.query(Group).join(admin_query, Group.id == admin_query.c.group).subquery()
	study_query = db.session.query(Study).join(group_query, Study.id == group_query.c.study).subquery()
	baselines = db.session.query(Baseline.sub_type, func.sum(Baseline.value)).join(study_query, Baseline.study == study_query.c.id)\
		.filter(Baseline.type != baseline_type.OTHER)\
		.group_by(Baseline.sub_type).all()

	return baselines


def get_treatment(treatment_name):
	treatment = db.session.query(Treatment)\
		.filter(Treatment.name == treatment_name)\
		.first()

	return treatment


'''
Gets the effects for a treatment.
Mode:
- strict: Only use the effects from studies purely focues on the treatment
- loose: Use any groups that have the treatment in it
'''
def get_effects(treatment_name, mode='strict'):
	treatment_query = db.session.query(Treatment).filter_by(name = treatment_name).subquery()

	if (mode == 'strict'):
		study_query = db.session.query(StudyTreatment).join(treatment_query, StudyTreatment.treatment == treatment_query.c.id).subquery()
		admin_query = db.session.query(EffectAdministration).join(treatment_query, EffectAdministration.treatment == treatment_query.c.id).subquery()
		group_query = db.session.query(EffectGroup).join(admin_query, EffectGroup.id == admin_query.c.group).subquery()
		effects = db.session.query(func.lower(Effect.name), func.sum(Effect.no_effected), func.sum(Effect.no_at_risk), func.count(distinct(Effect.study)))\
			.join(group_query, Effect.group == group_query.c.id)\
			.join(study_query, Effect.study == study_query.c.study)\
			.filter(Effect.no_effected > 0).group_by(func.lower(Effect.name)).all()
		return effects

	admin_query = db.session.query(EffectAdministration)\
		.join(treatment_query, EffectAdministration.treatment == treatment_query.c.id).subquery()
	group_query = db.session.query(EffectGroup)\
		.join(admin_query, EffectGroup.id == admin_query.c.group).subquery()
	effects = db.session.query(func.lower(Effect.name), func.sum(Effect.no_effected), func.sum(Effect.no_at_risk), func.count(Effect.study))\
		.join(group_query, Effect.group == group_query.c.id)\
		.filter(Effect.no_effected > 0).group_by(func.lower(Effect.name)).all()

	return effects


# The goal of this is to get a spread of all the scoring from studies
def get_scoring_spread(treatment_name, secondary_measures=False):
	treatment_query = db.session.query(Treatment).filter_by(name = treatment_name).subquery()
	study_treat_query = db.session.query(StudyTreatment).join(treatment_query, StudyTreatment.treatment == treatment_query.c.id).subquery()
	study_query = db.session.query(Study)\
		.join(study_treat_query, Study.id == study_treat_query.c.study)\
		.join(StudyTreatment, Study.id == StudyTreatment.study)\
		.group_by(Study.id)\
		.having(func.count(StudyTreatment.treatment) == 1).subquery()

	if (secondary_measures):
		analytics_and_measures = db.session.query(Analytics, Measure)\
			.join(study_query, Analytics.study == study_query.c.id)\
			.join(Measure, Analytics.measure == Measure.id).all()
		return analytics_and_measures

	analytics_and_measures = db.session.query(Analytics, Measure)\
		.join(study_query, Analytics.study == study_query.c.id)\
		.join(Measure, Analytics.measure == Measure.id)\
		.filter(Measure.type == measure_type.PRIMARY).all()

	return analytics_and_measures


def get_conditions(treatment_name):
	conditions = db.session.query(Condition, func.count(Study.id).label('no_studies'))\
		.join(StudyCondition, StudyCondition.condition == Condition.id)\
		.join(StudyTreatment, StudyTreatment.study == StudyCondition.study)\
		.join(Treatment, StudyTreatment.treatment == Treatment.id)\
		.where(Treatment.name == treatment_name)\
		.join(Study, Study.id == StudyTreatment.study)\
		.group_by(Condition.id)\
		.order_by(desc('no_studies'))\
		.all()

	return conditions


def get_no_studies(treatment_name):
	no_studies = db.session.query(func.count(StudyTreatment.study).label('no_studies'))\
		.join(Treatment, StudyTreatment.treatment == Treatment.id)\
		.filter(Treatment.name == treatment_name)\
		.all()

	return no_studies


def get_no_conditions(treatment_name):
	no_conditions = db.session.query(func.count(distinct(StudyCondition.condition)).label('no_conditions'))\
		.join(StudyTreatment, StudyTreatment.study == StudyCondition.study)\
		.join(Treatment, Treatment.id == StudyTreatment.treatment)\
		.filter(Treatment.name == treatment_name)\
		.all()

	return no_conditions


def get_condition_analytics(treatment_name, analytics=False, top=5):
	agg_conditions = db.session.query(Condition.id.label('conditions_id'), func.count(Analytics.id).label('no_analytics'))\
		.join(StudyCondition, StudyCondition.condition == Condition.id)\
		.join(StudyTreatment, StudyCondition.study == StudyTreatment.study)\
		.join(Treatment, Treatment.id == StudyTreatment.treatment)\
		.filter(Treatment.name == treatment_name)\
		.join(Analytics, StudyCondition.study == Analytics.study)\
		.group_by(Condition.id)\
		.order_by(desc('no_analytics'))\
		.limit(top)\
		.subquery() 

	condition_analytics = db.session.query(Condition, Analytics)\
		.join(agg_conditions, agg_conditions.c.conditions_id == Condition.id)\
		.join(StudyCondition, Condition.id == StudyCondition.condition)\
		.join(StudyTreatment, StudyCondition.study == StudyTreatment.study)\
		.join(Treatment, Treatment.id == StudyTreatment.treatment)\
		.filter(Treatment.name == treatment_name)\
		.join(Analytics, Analytics.study == StudyCondition.study)\
		.join(Measure, Analytics.measure == Measure.id)\
		.filter(Measure.type == measure_type.PRIMARY)\
		.all()

	return condition_analytics 


def get_study_analytics(treatment_name, request_args):
	condition_id = request_args.get('condition', '', type=int)

	analytics = db.session.query(Study, Analytics)\
		.join(StudyCondition, StudyCondition.study == Analytics.study)\
		.join(Study, Study.id == StudyCondition.study)

	if (condition_id != ''):
		analytics = analytics.where(StudyCondition.condition == condition_id)

	study_analytics = analytics \
		.join(StudyTreatment, StudyCondition.study == StudyTreatment.study)\
		.join(Treatment, Treatment.id == StudyTreatment.treatment)\
		.filter(Treatment.name == treatment_name)\
		.join(Measure, Analytics.measure == Measure.id)\
		.filter(Measure.type == measure_type.PRIMARY)\
		.all()

	return study_analytics 


def get_analytics(treatment_name, request_args):
	condition_id = request_args.get('condition', '', type=int)

	analytics = db.session.query(Analytics)\
		.join(StudyCondition, StudyCondition.study == Analytics.study)

	if (condition_id != ''):
		analytics = analytics.where(StudyCondition.condition == condition_id)

	analytics = analytics \
		.join(StudyTreatment, StudyCondition.study == StudyTreatment.study)\
		.join(Treatment, Treatment.id == StudyTreatment.treatment)\
		.filter(Treatment.name == treatment_name)\
		.join(Measure, Analytics.measure == Measure.id)\
		.filter(Measure.type == measure_type.PRIMARY)\
		.all()

	return analytics 


def get_condition_scoring(treatment_name):
	treatment_query = db.session.query(Treatment).filter_by(name = treatment_name).subquery()
	codntion_scores = db.session.query(ConditionScore, Condition).join(treatment_query, ConditionScore.treatment == treatment_query.c.id)\
		.join(Condition, Condition.id == ConditionScore.condition).all()

	return codntion_scores
