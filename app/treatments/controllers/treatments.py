from app.treatments.models import Baseline, Treatment, Administration, Study, Group,\
	Effect, EffectGroup, EffectAdministration, Condition, StudyCondition, Comparison, Analytics,\
	ConditionScore
from app import db
from sqlalchemy.orm import aliased
from sqlalchemy import func


def get_demographics(treatment_name):
	treatment_query = db.session.query(Treatment).filter_by(name = treatment_name).subquery()
	admin_query = db.session.query(Administration).join(treatment_query, Administration.treatment == treatment_query.c.id).subquery()
	group_query = db.session.query(Group).join(admin_query, Group.id == admin_query.c.group).subquery()
	study_query = db.session.query(Study).join(group_query, Study.id == group_query.c.study).subquery()
	baselines = db.session.query(Baseline).join(study_query, Baseline.study == study_query.c.id).all()

	return [baseline for baseline in baselines if baseline.is_demographic()]


def get_effects(treatment_name):
	treatment_query = db.session.query(Treatment).filter_by(name = treatment_name).subquery()
	admin_query = db.session.query(EffectAdministration).join(treatment_query, EffectAdministration.treatment == treatment_query.c.id).subquery()
	group_query = db.session.query(EffectGroup).join(admin_query, EffectGroup.id == admin_query.c.group).subquery()
	effects = db.session.query(Effect).join(group_query, Effect.group == group_query.c.id)\
		.filter(Effect.no_effected > 0).all()

	return effects


def get_conditions_and_counts(treatment_name):
	treatment_query = db.session.query(Treatment).filter_by(name = treatment_name).subquery()
	admin_query = db.session.query(Administration).join(treatment_query, Administration.treatment == treatment_query.c.id).subquery()
	group_query = db.session.query(Group).join(admin_query, Group.id == admin_query.c.group).subquery()
	study_query = db.session.query(Study).join(group_query, Study.id == group_query.c.study).subquery()
	study_conditions_query = db.session.query(StudyCondition)\
		.join(study_query, StudyCondition.study == study_query.c.id).subquery()
	conditions_and_counts = db.session.query(Condition, func.count(study_conditions_query.c.study)).select_from(study_conditions_query)\
		.join(Condition, Condition.id == study_conditions_query.c.condition, isouter=True)\
		.group_by(Condition.id).all()

	return conditions_and_counts


def get_condition_scoring(treatment_name):
	treatment_query = db.session.query(Treatment).filter_by(name = treatment_name).subquery()
	codntion_scores = db.session.query(ConditionScore, Condition).join(treatment_query, ConditionScore.treatment == treatment_query.c.id)\
		.join(Condition, Condition.id == ConditionScore.condition).all()

	return codntion_scores
