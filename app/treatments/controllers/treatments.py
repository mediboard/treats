from app.treatments.models import Baseline, Treatment, Administration, Study, Group,\
	Effect, EffectGroup, EffectAdministration, Condition, StudyCondition, Comparison, Analytics,\
	ConditionScore, StudyTreatment, Measure
from app.treatments.models import baseline_type, measure_type
from app import db
from sqlalchemy.orm import aliased, Bundle
from sqlalchemy import func, distinct
import sqlalchemy as sa


def get_demographics(treatment_name):
	treatment_query = db.session.query(Treatment).filter_by(name = treatment_name).subquery()
	admin_query = db.session.query(Administration).join(treatment_query, Administration.treatment == treatment_query.c.id).subquery()
	group_query = db.session.query(Group).join(admin_query, Group.id == admin_query.c.group).subquery()
	study_query = db.session.query(Study).join(group_query, Study.id == group_query.c.study).subquery()
	baselines = db.session.query(Baseline.sub_type, func.sum(Baseline.value)).join(study_query, Baseline.study == study_query.c.id)\
		.filter(Baseline.type != baseline_type.OTHER)\
		.group_by(Baseline.sub_type).all()

	return baselines

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

	admin_query = db.session.query(EffectAdministration).join(treatment_query, EffectAdministration.treatment == treatment_query.c.id).subquery()
	group_query = db.session.query(EffectGroup).join(admin_query, EffectGroup.id == admin_query.c.group).subquery()
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


# TODO: this is super slow (4 sec execution) - speed this up
def get_conditions(treatment_name, analytics=False):
	treatment_query = db.session.query(Treatment).filter_by(name = treatment_name).subquery()
	admin_query = db.session.query(Administration).join(treatment_query, Administration.treatment == treatment_query.c.id).subquery()
	group_query = db.session.query(Group).join(admin_query, Group.id == admin_query.c.group).subquery()
	study_query = db.session.query(Study).join(group_query, Study.id == group_query.c.study).subquery()

	study_conditions_query = db.session.query(StudyCondition)\
		.join(study_query, StudyCondition.study == study_query.c.id).subquery()

	if (analytics):
		condition_analytics_counts = db.session.query(Condition, Analytics)\
			.join(study_conditions_query, study_conditions_query.c.condition == Condition.id)\
			.add_columns(Condition.no_studies)\
			.join(Analytics, Analytics.study == study_conditions_query.c.study)\
			.join(Measure, Analytics.measure == Measure.id)\
			.filter(Measure.type == measure_type.PRIMARY)\
			.all()

		return condition_analytics_counts

	return conditions.all()

def get_condition_scoring(treatment_name):
	treatment_query = db.session.query(Treatment).filter_by(name = treatment_name).subquery()
	codntion_scores = db.session.query(ConditionScore, Condition).join(treatment_query, ConditionScore.treatment == treatment_query.c.id)\
		.join(Condition, Condition.id == ConditionScore.condition).all()

	return codntion_scores
