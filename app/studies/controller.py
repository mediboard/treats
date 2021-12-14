from app import db
from app.models import Study, Criteria, Measure, Analytics, Baseline,\
	Group, StudyTreatment, StudyCondition
from sqlalchemy.orm import joinedload, raiseload


def get_study(study_id):
	studies = db.session.query(Study)\
		.filter_by(id = study_id)\
		.options(
			joinedload(Study.criteria),
			joinedload(Study.measures).joinedload(Measure.outcomes),
			joinedload(Study.analytics).joinedload(Analytics.groups),
			joinedload(Study.baselines),
			joinedload(Study.groups),
			joinedload(Study.conditions).joinedload(StudyCondition.conditions),
			joinedload(Study.treatments).joinedload(StudyTreatment.treatments),
			raiseload('*')
		)

	return studies.all()


def get_baselines(study_id):
	baselines = db.session.query(Baseline)\
		.filter_by(study = study_id)

	return baselines.all()


def get_measures(study_id):
	measures = db.session.query(Measure)
		.filter_by(study = study_id)
		.options(
			joinedload(Measure.outcomes),
			raiseload('*')
		)

	return measures.all()


def get_groups(study_id):
	groups = db.session.query(Group)
		.filter_by(study = study_id)

	return groups.all()


def get_criteria(study_id):
	criteria = db.session.query(Criteria)
		.filter_by(study = study_id)

	return criteria.all()


def get_conditions(study_id):
	study_conditions = db.session.query(StudyCondition)
		.filter_by(study = study_id).subquery()

	conditions = db.session.query(Condition)
		.join(study_conditions, Condition.id == study_conditions.condition)

	return conditions.all()


def get_treatments(study_id):
	study_treatments = db.session.query(StudyTreatment)
		.filter_by(study = study_id).subquery()

	treatments = db.session.query(Treatment)
		.join(study_treatments, Treatment.id == study_treatments.treatment)

	return treatments.all()
