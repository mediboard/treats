from app import db
from app.models import Study, Criteria, Measure, Analytics, Baseline,\
	Group, StudyTreatment, StudyCondition, Condition, Treatment, Effect, EffectGroup, EffectAdministration, ConditionGroup, Administration
from sqlalchemy.orm import joinedload, raiseload
from sqlalchemy import and_, func, or_


ROWS_PER_PAGE=10

def search(query, limit=10):
	processedQuery = query.replace(' ', ' & ') if query[-1] != ' ' else query
	studies = db.session.query(Study)\
		.filter(func.lower(Study.short_title).match(processedQuery) | func.lower(Study.short_title).like(f'%{processedQuery}%'))\
		.limit(limit)\
		.all()

	return studies


def get_banner_studies():
	banner_studies = db.session.query(Study)\
		.filter(Study.id.in_(['NCT01014533', 'NCT00392041', 'NCT00386334', 'NCT03262038', 'NCT02944656']))\
		.all()

	return banner_studies


def get_studies(args, page=1, subquery=False):
	# Need to filter by search string, condition(s), treatment(s), size, kids
	studies = db.session.query(Study)

	query = args.get('q')
	if (query):
		processedQuery = query.replace(' ', ' & ') if query[-1] != ' ' else query
		studies = studies.filter(func.lower(Study.short_title).match(processedQuery) | func.lower(Study.short_title).like(f'%{processedQuery}%'))\
	
	min_age = args.get('min_age', None, type=int)
	min_age_units = args.get('min_age_units', None, type=str)
	max_age = args.get('max_age', None, type=int)
	max_age_units = args.get('max_age_units', None, type=str)

	if (min_age and min_age != -1 and min_age_units):
		# Minimum bound
		min_age_years = min_age if min_age_units == "YEARS" else min_age / 12.0
		min_age_months = min_age if min_age_units == "MONTHS" else min_age * 12.0

		studies = studies.filter(
			or_(and_(func.lower(Study.min_age_units).match("YEARS"), Study.min_age >= min_age_years),
				and_(func.lower(Study.min_age_units).match("MONTHS"),Study.min_age >= min_age_months)))

	if (max_age and max_age != -1 and max_age_units):
		# Maximum bound
		max_age_years = max_age if max_age_units == "YEARS" else max_age / 12.0
		max_age_months = max_age if max_age_units == "MONTHS" else max_age * 12.0

		studies = studies.filter(
			or_(and_(func.lower(Study.max_age_units).match("YEARS"), Study.max_age <= max_age_years, Study.max_age != -1),
				and_(func.lower(Study.max_age_units).match("MONTHS"),Study.max_age <= max_age_months, Study.max_age != -1)))

	condition = args.get('condition', None, type=str)
	if (condition):
		studies = studies.join(StudyCondition, StudyCondition.study == Study.id)\
			.join(Condition, Condition.id == StudyCondition.condition)\
			.filter(func.lower(Condition.name).match(condition) | func.lower(Condition.name).like(f'%{condition}%'))

	condition_group = args.get('condition_group', None, type=str)
	if (condition_group):
		studies = studies.join(StudyCondition, StudyCondition.study == Study.id)\
			.join(Condition, Condition.id == StudyCondition.condition)\
			.join(ConditionGroup, ConditionGroup.id == Condition.condition_group)\
			.filter(func.lower(ConditionGroup.name).match(condition_group) | func.lower(ConditionGroup.name).like(f'%{condition_group}%'))

	treatment = args.get('treatment', None, type=str)
	if (treatment):
		studies = studies.join(StudyTreatment, StudyTreatment.study == Study.id)\
			.join(Treatment, Treatment.id == StudyTreatment.treatment)\
			.filter(func.lower(Treatment.name).match(treatment) | func.lower(Treatment.name).like(f'%{treatment}%'))

	gender = args.get('gender', None, type=str)
	if (gender):
		studies = studies.filter(Study.gender == gender)

	studies = studies.options(
		joinedload(Study.conditions).joinedload(StudyCondition.conditions),
		joinedload(Study.treatments).joinedload(StudyTreatment.treatments),
		joinedload(Study.effects),
		raiseload('*')
	)

	if (subquery):
		return studies.subquery()

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


def get_effects(study_id):
	effect_groups = db.session.query(EffectGroup)\
		.filter(EffectGroup.study == study_id)\
		.options(
			joinedload(EffectGroup.effects),
			joinedload(EffectGroup.administrations).joinedload(EffectAdministration.treatments),
			raiseload('*'))

	return effect_groups.all()


def add_admin(admin_data):
	new_id = db.session.query(func.max(Administration.id)).first()[0] + 1

	new_admin = Administration()
	new_admin.from_dict({**admin_data, 'id': new_id})


	db.session.add(new_admin)
	db.session.commit()

	return new_admin 


def remove_admin(admin_id):
	to_delete = db.session.query(Administration)\
		.filter(Administration.id == admin_id)\
		.first()

	db.session.delete(to_delete)
	db.session.commit()


def get_measures(study_id):
	measures = db.session.query(Measure)\
		.filter_by(study = study_id)

	return measures.all()


def get_groups(study_id):
	groups = db.session.query(Group)\
		.options(joinedload(Group.administrations).joinedload(Administration.treatments))\
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
