from app import db
from app.models import Study, Criteria, Measure, Analytics, Baseline,\
	Group, StudyTreatment, StudyCondition, Condition, Treatment
from sqlalchemy.orm import joinedload, raiseload
from sqlalchemy import func


def search(query, limit=10):
	processedQuery = query.replace(' ', ' & ') if query[-1] != ' ' else query
	studies = db.session.query(Study)\
		.filter(func.lower(Study.short_title).match(processedQuery) | func.lower(Study.short_title).like(f'%{processedQuery}%'))\
		.limit(limit)\
		.all()

	return studies


def get_study(study_id):
	studies = db.session.query(Study)\
		.filter_by(id = study_id)\

	return studies.all()


def get_study_summary(study_id):
	# Need conditions, treatments, participants
	studies = db.session.query(Study)\
		.filter_by(id = study_id)\
		.options(
			joinedload(Study.conditions).joinedload(StudyCondition.conditions),
			raiseload('*')
		).all()

	return studies


def get_baselines(study_id):
	baselines = db.session.query(Baseline)\
		.filter_by(study = study_id)

	return baselines.all()


def get_measures(study_id):
	measures = db.session.query(Measure)\
		.filter_by(study = study_id)\
		.options(
			joinedload(Measure.outcomes),
			joinedload(Measure.analytics).joinedload(Analytics.groups),
			raiseload('*')
		)

	return measures.all()


def get_groups(study_id):
	groups = db.session.query(Group)\
		.filter_by(study = study_id)

	return groups.all()


def get_criteria(study_id):
	criteria = db.session.query(Criteria)\
		.filter_by(study = study_id)

	return criteria.all()


def get_conditions(study_id):
	study_conditions = db.session.query(StudyCondition)\
		.filter_by(study = study_id).subquery()

	conditions = db.session.query(Condition)\
		.join(study_conditions, Condition.id == study_conditions.c.condition)

	return conditions.all()


def get_treatments(study_id):
	study_treatments = db.session.query(StudyTreatment)\
		.filter_by(study = study_id).subquery()

	treatments = db.session.query(Treatment)\
		.join(study_treatments, Treatment.id == study_treatments.c.treatment)

	return treatments.all()
