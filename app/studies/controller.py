from app import db
from app.models import Study, Criteria, Measure, Analytics, Baseline,\
	Group, StudyTreatment, StudyCondition, Condition, Treatment, Effect, EffectGroup, EffectAdministration
from sqlalchemy.orm import joinedload, raiseload
from sqlalchemy import func


ROWS_PER_PAGE=10

def search(query, limit=10):
	processedQuery = query.replace(' ', ' & ') if query[-1] != ' ' else query
	studies = db.session.query(Study)\
		.filter(func.lower(Study.short_title).match(processedQuery) | func.lower(Study.short_title).like(f'%{processedQuery}%'))\
		.limit(limit)\
		.all()

	return studies


def get_studies(args, page=1):
	# Need to filter by search string, condition(s), treatment(s), size, kids
	studies = db.session.query(Study)

	query = args.get('q')
	if (query):
		processedQuery = query.replace(' ', ' & ') if query[-1] != ' ' else query
		studies = studies.filter(func.lower(Study.short_title).match(processedQuery) | func.lower(Study.short_title).like(f'%{processedQuery}%'))\

	conditions = args.get('conditions', None, type=str)
	if (conditions):
		studies = studies.join(StudyCondition, StudyCondition.study == Study.id)\
			.filter(StudyCondition.condition.in_(conditions.split(',')))

	treatments = args.get('treatments', None, type=str)
	if (treatments):
		studies = studies.join(StudyTreatment, StudyTreatment.study == Study.id)\
			.filter(StudyTreatment.treatment.in_(treatments.split(',')))

	gender = args.get('gender', None, type=str)
	if (gender):
		studies = studies.filter(Study.gender == gender)

	studies = studies.options(
		joinedload(Study.conditions).joinedload(StudyCondition.conditions),
		joinedload(Study.treatments).joinedload(StudyTreatment.treatments),
		raiseload('*')
	)

	studies = studies.paginate(page, ROWS_PER_PAGE)

	return studies.items, studies.next_num, studies.total


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


def get_effects_by_group(group_id):
	effect_groups = db.session.query(EffectGroup)\
		.filter(EffectGroup.id == group_id)\
		.options(
			joinedload(EffectGroup.effects),
			joinedload(EffectGroup.administrations).joinedload(EffectAdministration.treatments),
			raiseload('*'))

	return effect_groups.all()


def get_effects(study_id):
	effect_groups = db.session.query(EffectGroup)\
		.filter(EffectGroup.study == study_id)\
		.options(
			joinedload(EffectGroup.effects),
			joinedload(EffectGroup.administrations).joinedload(EffectAdministration.treatments),
			raiseload('*'))

	return effect_groups.all()


def get_measures(study_id):
	measures = db.session.query(Measure)\
		.filter_by(study = study_id)

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


def get_studies_by_ids(study_ids):
	studies = db.session.query(Study, func.avg(Analytics.p_value).label('mean'), func.min(Analytics.p_value).label('min'))\
		.join(Analytics, Analytics.study == Study.id)\
		.filter(Study.id.in_(study_ids))\
		.group_by(Study.id)

	return studies.all()
