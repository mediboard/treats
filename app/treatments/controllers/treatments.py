import asyncio
from app.models import Baseline, Treatment, Administration, Study, Group,\
	Effect, EffectGroup, EffectAdministration, Condition, StudyCondition, Comparison, Analytics,\
	ConditionScore, StudyTreatment, Measure, Outcome, MeasureGroup, MeasureGroupMeasure, EffectCluster, ConditionGroup
from app.models import baseline_type, measure_type
from app import db
from sqlalchemy.orm import aliased, lazyload, contains_eager, joinedload, raiseload
from sqlalchemy import func, distinct, desc, or_, text, case, literal_column
from app.treatments.controllers.statistics import pick_top_point, non_calculable, cohen_d
import sqlalchemy as sa
from app.studies.controller import get_studies
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import aggregate_order_by


ROWS_PER_PAGE=10

def search_treatments(query, limit=5):
	processedQuery = query.replace(' ', ' & ') if query[-1] != ' ' else query
	results = db.session.query(Treatment)\
		.filter(func.lower(Treatment.name).match(processedQuery) | func.lower(Treatment.name).like(f'%{processedQuery}%'))\
		.order_by(desc(Treatment.no_studies))\
		.limit(limit)\
		.all()

	return results


def search_measures(treatment_name, condition_id, query, limit=5):
	processedQuery = query.replace(' ', ' & ') if query[-1] != ' ' else query

	results = db.session.query(Measure)\
		.join(Study, Study.id == Measure.study)\
		.join(StudyCondition, StudyCondition.study == Study.id)\
		.join(Group, Group.study == Study.id)\
		.join(Administration, Administration.group == Group.id)\
		.join(Treatment, Treatment.id == Administration.treatment)\
		.filter(StudyCondition.condition == condition_id)\
		.filter(Treatment.name == treatment_name)\
		.filter(func.lower(Measure.title).match(processedQuery) | func.lower(Measure.title).like(f'%{processedQuery}%'))\
		.limit(limit)

	return results.all();


def get_top_treatments():
	top_treatments = ['Ketamine', 'Gabapentin', 'Pregabalin', 'Citalopram', 'Fluoxetine', 'Estradiol']
	results = db.session.query(Treatment)\
		.filter(Treatment.name.in_(top_treatments))\
		.order_by(desc(Treatment.no_studies))\
		.all()

	return results


def create_treatment(treatment_data):
	new_id = db.session.query(func.max(Treatment.id)).first()[0] + 1

	new_treatment = Treatment()
	new_treatment.from_dict({'id': new_id, **treatment_data})

	db.session.add(new_treatment)
	db.session.commit()

	return new_treatment


def get_demographics(treatment_name, args=None):

	baselines = db.session.query(Baseline.sub_type, func.sum(Baseline.value))\

	if (args):
		study_subquery = get_studies(args, subquery=True)
		baselines = baselines.join(study_query, study_query.c.id == Baseline.study)

	baselines = baselines.join(StudyTreatment, StudyTreatment.study == Baseline.study)\
		.join(Treatment, Treatment.id == StudyTreatment.treatment)\
		.filter(Treatment.name == treatment_name)\
		.filter(Baseline.type != baseline_type.OTHER)\
		.group_by(Baseline.sub_type).all()

	return baselines


def get_treatment(treatment_name):
	treatment = db.session.query(Treatment)\
		.filter(Treatment.name == treatment_name)\
		.first()

	return treatment


def get_effects(treatment_name, limit=0, args=None):
	single_groups = db.session.query(EffectGroup)\
		.join(EffectAdministration, EffectAdministration.group == EffectGroup.id)\
		.join(Treatment, Treatment.id == EffectAdministration.treatment)\
		.filter(Treatment.name == treatment_name)\
		.subquery()

	effects = db.session.query(EffectCluster.name, func.sum(Effect.no_effected), func.sum(Effect.no_at_risk), func.count(distinct(Effect.study)), func.string_agg(Effect.study, aggregate_order_by(literal_column("','"), Effect.study)))\
		.join(EffectCluster, Effect.cluster == EffectCluster.id)\
		.join(single_groups, single_groups.c.id == Effect.group)\
		.filter(Effect.no_effected > 0)\

	if (args):
		filtering_studies = get_studies(args, subquery=True)
		effects = effects.join(filtering_studies, filtering_studies.c.id == Effect.study)

	effects = effects.group_by(EffectCluster.name).all()

	if limit != 0:
		# Sort based on frequency when side effect exists in > 1 studies to handle false positives
		effects.sort(key=lambda x: 0 if x[2] == 0 or x[3] < 2 else -x[1] / x[2])
		effects = effects[:limit]

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


def get_no_analytics(treatment_name, condition_group=None):
	# Get the number of statistically significant datapoints
	base_query = db.session.query(func.count(distinct(Analytics.id)).label('no_analytics'))\
		.join(Comparison, Comparison.analytic == Analytics.id)\
		.join(Group, Comparison.group == Group.id)\
		.join(Administration, Administration.group == Group.id)\
		.join(Treatment, Administration.treatment == Treatment.id)

	if (condition_group):
		base_query = base_query\
			.join(StudyCondition, StudyCondition.study == Group.study)\
			.join(Condition, Condition.id == StudyCondition.condition)\
			.join(ConditionGroup, ConditionGroup.id == Condition.condition_group)\
			.filter(ConditionGroup.name == condition_group)

	no_analytics = base_query\
		.filter(Treatment.name == treatment_name)\
		.all()

	return no_analytics[0]


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


def get_analytic_outcomes(analytic_id):
	results = db.session.query(Group, Outcome)\
		.join(Comparison, Comparison.group == Group.id)\
		.join(Analytics, Analytics.id == Comparison.analytic)\
		.join(Outcome, Group.id == Outcome.group)\
		.filter(Analytics.id == analytic_id)\
		.filter(Outcome.measure == Analytics.measure)\
		.all()

	return results


def get_placebo_analytics(measure_id, treatment_id):
	results = db.session.query(Analytics, Treatment)\
		.filter(Analytics.measure == measure_id)\
		.join(Comparison, Comparison.analytic == Analytics.id)\
		.join(Group, Comparison.group == Group.id)\
		.join(Administration, Administration.group == Group.id)\
		.join(Treatment, Treatment.id == Administration.treatment)\
		.all()

	# Filtering out the analytics that dont compare placebo to treatment
	analytic2treats = {}
	analytics_to_delete = []
	for analytic, treatment in results:
		if analytic.id not in analytic2treats:
			analytic2treats[analytic.id] = {'analytic': analytic.to_small_dict(), 'treatments': []}

		if (treatment.id != treatment_id) and (treatment.id == ''):
			analytics_to_delete.append(analytic.id)

		analytic2treats[analytic.id]['treatments'].append(treatment.to_dict())

	for analytic_id in list(set(analytics_to_delete)):
		del analytic2treats[analytic_id]

	return [x['analytic'] for x in analytic2treats.values()]


def get_measures_data(treatment_id, measure_ids):
	bunch_of_data = db.session.query(Measure, Group)\
		.filter(Measure.id.in_(measure_ids))\
		.join(Outcome, Outcome.measure == Measure.id)\
		.join(Group, Group.id == Outcome.group)\
		.options(
			contains_eager(Measure.outcomes),
			joinedload(Group.treatments),
			raiseload('*'))\
		.order_by(case([
			(Measure.type == measure_type.PRIMARY, 1),
			(Measure.type == measure_type.SECONDARY, 2)
		])).all()

	# put all the measure outcomes into their groups
	# filter out all groups that don't have the treatment or a placebo
	id2Group = {}
	id2Measure = {}
	for measure, group in bunch_of_data:
		if (group.id not in id2Group):
			id2Group[group.id] = group.to_dict()

		if (measure.id not in id2Measure):
			id2Measure[measure.id] = measure


	measures_outcomes = []
	calculable_measures = [measure for measure in id2Measure.values() if str(measure.dispersion) not in non_calculable]
	for measure in calculable_measures:
		group2outcome = {}

		for outcome in measure.outcomes:
			if outcome.group not in group2outcome:
				group2outcome[outcome.group] = { 
					**id2Group[outcome.group],
					'outcomes': []
				}

			group2outcome[outcome.group]['outcomes'].append(outcome)

		measures_outcomes.append({
			**measure.to_small_dict(),
			'groups': [x for x in group2outcome.values()]
		})

	comparisons = []
	for measure in measures_outcomes:
		for i in range(len(measure['groups'])):
			for j in range(i, len(measure['groups'])):
				group_a = measure['groups'][i]
				group_b = measure['groups'][j]

				group_a_is_treat = group_a['administrations'][0]['id'] == treatment_id
				group_a_is_compare = group_a['administrations'][0]['id'] == 2182

				group_b_is_treat = group_b['administrations'][0]['id'] == treatment_id
				group_b_is_compare = group_b['administrations'][0]['id'] == 2182

				if ((group_a_is_treat and group_b_is_treat) or (group_a_is_compare and group_b_is_compare)):
					continue

				treat_group = group_a if group_a_is_treat else group_b
				compare_group = group_a if group_a_is_compare else group_b

				outcome_a = treat_group['outcomes'][0]
				outcome_b = compare_group['outcomes'][0]

				if (treat_group['outcomes'][0].title != 'NA'):
					outcome_a, outcome_b = pick_top_point(treat_group['outcomes'], compare_group['outcomes'], measure['dispersion'])

				d = cohen_d(outcome_a, outcome_b, measure['dispersion'])
				if d == 0:
					continue

				comparisons.append({
					'compare_title': compare_group['title'],
					'compare_outcome_id': outcome_b.id,
					'treat_title': treat_group['title'],
					'treat_outcome_id': outcome_a.id,
					'measure_title': measure['title'],
					'study': measure['study'],
					'cohen_d': d
				})

	return comparisons 


def get_measure(measure_id):
	measure = db.session.query(Measure)\
		.filter(Measure.id == measure_id)\
		.first()

	return measure


# I think we need to pre-compute a diff_table
def get_treatment_diffs(treatment_id):
	# Get the comparisons where thr groups diff by treatment
	# Sort ascending by diff size

	# Get all groups with treament
	# Get all groups in same studies without treatment

	# We nee to get the treatments in each comp and diff them
	# Diff teh strings in positive vs negative
	positive_comps = db.session.query(Comparison, func.string_agg(Treatment.name, aggregate_order_by(literal_column("'%'"), Treatment.name)).label('pos_treats'))\
		.join(Group, Group.id == Comparison.group)\
		.join(Administration, Administration.group == Group.id)\
		.join(Treatment, Treatment.id == Administration.treatment)\
		.filter(Treatment.id == treatment_id)\
		.group_by(Comparison.id)\
		.subquery()

	negative_comps = db.session.query(Comparison, func.string_agg(Treatment.name, aggregate_order_by(literal_column("'%'"), Treatment.name)).label('neg_treats'))\
		.join(Group, Group.id == Comparison.group)\
		.filter(~Group.treatments.any(Treatment.id == treatment_id))\
		.join(Administration, Administration.group == Group.id)\
		.join(Treatment, Treatment.id == Administration.treatment)\
		.group_by(Comparison.id)\
		.subquery()

	stuff = db.session.query(
		Analytics,
		func.string_agg(func.concat(negative_comps.c.neg_treats,positive_comps.c.pos_treats), '$').label('treat_comps'))\
		.join(negative_comps, negative_comps.c.analytic == Analytics.id)\
		.join(positive_comps, positive_comps.c.analytic == negative_comps.c.analytic)\
		.filter(negative_comps.c.neg_treats != '')\
		.filter(positive_comps.c.pos_treats != '')\
		.group_by(Analytics.id)\
		.all()

	print(stuff)


def get_placebo_group_outcomes(treatment_id, condition_group_id, measure_group_id = 1):
	study_query = db.session.query(Study)\
		.join(StudyTreatment, StudyTreatment.study == Study.id)\
		.filter(StudyTreatment.treatment == treatment_id)\
		.join(StudyCondition, StudyCondition.study == StudyTreatment.study)\
		.join(Condition, StudyCondition.condition == Condition.id)\
		.group_by(Study.id)\
		.having(func.count(distinct(Condition.condition_group)) == 1)\
		.subquery()

	bunch_of_data = db.session.query(Measure, Group)\
		.join(MeasureGroupMeasure, MeasureGroupMeasure.measure == Measure.id)\
		.join(MeasureGroup, MeasureGroup.id == MeasureGroupMeasure.measureGroup)\
		.filter(MeasureGroup.id == measure_group_id)\
		.join(Outcome, Outcome.measure == Measure.id)\
		.join(Group, Group.id == Outcome.group)\
		.join(study_query, study_query.c.id == Group.study)\
		.join(StudyCondition, StudyCondition.study == study_query.c.id)\
		.join(Condition, StudyCondition.condition == Condition.id)\
		.filter(Condition.condition_group == condition_group_id)\
		.options(
			contains_eager(Measure.outcomes),
			joinedload(Group.administrations).joinedload(Administration.treatments),
			raiseload('*'))\
		.order_by(case([
			(Measure.type == measure_type.PRIMARY, 1),
			(Measure.type == measure_type.SECONDARY, 2)
		])).all()

	# put all the measure outcomes into their groups
	# filter out all groups that don't have the treatment or a placebo
	id2Group = {}
	id2Measure = {}
	for measure, group in bunch_of_data:
		if (group.id not in id2Group):
			id2Group[group.id] = group.to_dict()

		if (measure.id not in id2Measure):
			id2Measure[measure.id] = measure


	measures_outcomes = []
	calculable_measures = [measure for measure in id2Measure.values() if str(measure.dispersion) not in non_calculable]
	for measure in calculable_measures:
		group2outcome = {}

		for outcome in measure.outcomes:
			if outcome.group not in group2outcome:
				group2outcome[outcome.group] = { 
					**id2Group[outcome.group],
					'outcomes': []
				}

			group2outcome[outcome.group]['outcomes'].append(outcome)

		measures_outcomes.append({
			**measure.to_small_dict(),
			'groups': [x for x in group2outcome.values()]
		})

	comparisons = []
	for measure in measures_outcomes:
		for i in range(len(measure['groups'])):
			for j in range(i, len(measure['groups'])):
				group_a = measure['groups'][i]
				group_b = measure['groups'][j]

				group_a_is_treat = group_a['administrations'][0]['id'] == treatment_id
				group_a_is_compare = group_a['administrations'][0]['id'] == 2182

				group_b_is_treat = group_b['administrations'][0]['id'] == treatment_id
				group_b_is_compare = group_b['administrations'][0]['id'] == 2182

				if ((group_a_is_treat and group_b_is_treat) or (group_a_is_compare and group_b_is_compare)):
					continue

				treat_group = group_a if group_a_is_treat else group_b
				compare_group = group_a if group_a_is_compare else group_b

				outcome_a = treat_group['outcomes'][0]
				outcome_b = compare_group['outcomes'][0]

				if (treat_group['outcomes'][0].title != 'NA'):
					outcome_a, outcome_b = pick_top_point(treat_group['outcomes'], compare_group['outcomes'], measure['dispersion'])

				d = cohen_d(outcome_a, outcome_b, measure['dispersion'])
				if d == 0:
					continue

				comparisons.append({
					'compare_title': compare_group['title'],
					'compare_outcome_id': outcome_b.id,
					'treat_title': treat_group['title'],
					'treat_outcome_id': outcome_a.id,
					'measure_title': measure['title'],
					'study': measure['study'],
					'cohen_d': d
				})

	return comparisons 


def get_placebo_measure_groups(treatment_id, condition_id):
	study_query = db.session.query(Study)\
		.join(StudyTreatment, StudyTreatment.study == Study.id)\
		.filter(StudyTreatment.treatment == treatment_id)\
		.join(StudyCondition, StudyCondition.study == StudyTreatment.study)\
		.group_by(Study.id)\
		.having(func.count(StudyCondition.id) == 1)\
		.subquery()


	measure_admins = db.session.query(Measure, Administration)\
		.join(Outcome, Outcome.measure == Measure.id)\
		.join(Group, Group.id == Outcome.group)\
		.join(study_query, study_query.c.id == Group.study)\
		.join(StudyCondition, StudyCondition.study == study_query.c.id)\
		.filter(StudyCondition.condition == condition_id)\
		.join(Administration, Administration.group == Group.id)\
		.order_by(case([
			(Measure.type == measure_type.PRIMARY, 1),
			(Measure.type == measure_type.SECONDARY, 2)
		]))\
		.all()

	measure2admins = {}
	for measure, admin in measure_admins:
		if measure.id not in measure2admins:
			measure2admins[measure.id] = {'measure': measure.to_small_dict(), 'hasTreat': False, 'hasControl': False}


		measure2admins[measure.id]['hasTreat'] = measure2admins[measure.id]['hasTreat'] or admin.treatment == treatment_id
		measure2admins[measure.id]['hasControl'] = measure2admins[measure.id]['hasControl'] or admin.treatment == 2182 

	measures = [measure['measure'] for measure in measure2admins.values() if measure['hasTreat'] and measure['hasControl']]

	# Get the placebo analytics
	results = db.session.query(Analytics, Treatment)\
		.filter(Analytics.measure.in_([measure['id'] for measure in measures]))\
		.join(Comparison, Comparison.analytic == Analytics.id)\
		.join(Group, Comparison.group == Group.id)\
		.join(Administration, Administration.group == Group.id)\
		.join(Treatment, Treatment.id == Administration.treatment).all()

	# Filtering out the analytics that dont compare placebo to treatment
	analytic2treats = {}
	analytics_to_delete = []
	for analytic, treatment in results:
		if analytic.id not in analytic2treats:
			analytic2treats[analytic.id] = {'analytic': analytic.to_small_dict(), 'treatments': []}

		if (treatment.id != treatment_id) and (treatment.id == ''):
			analytics_to_delete.append(analytic.id)

		analytic2treats[analytic.id]['treatments'].append(treatment.to_dict())

	for analytic_id in list(set(analytics_to_delete)):
		del analytic2treats[analytic_id]

	measure2Analytic = {measure['id']: {**measure, 'analytics': []} for measure in measures}
	for analytic in analytic2treats.values():
		measure2Analytic[analytic['analytic']['measure']]['analytics'].append(analytic['analytic'])

	# Put the measurements into groups
	group2measure = {}
	for measure in measure2Analytic.values():
		for group in measure['measureGroups']:
			if group['id'] not in group2measure:
				group2measure[group['id']] = {**group, 'measures': []}

			group2measure[group['id']]['measures'].append(measure)


	return [x for x in group2measure.values()]


def get_placebo_measures(treatment_id, condition_id, page=1):
	measure_admins = db.session.query(Measure, Administration)\
		.join(Outcome, Outcome.measure == Measure.id)\
		.join(Group, Group.id == Outcome.group)\
		.join(StudyTreatment, StudyTreatment.study == Group.study)\
		.filter(StudyTreatment.treatment == treatment_id)\
		.join(StudyCondition, StudyCondition.study == StudyTreatment.study)\
		.filter(StudyCondition.condition == condition_id)\
		.join(Administration, Administration.group == Group.id)\
		.order_by(case([
			(Measure.type == measure_type.PRIMARY, 1),
			(Measure.type == measure_type.SECONDARY, 2)
		]))\
		.all()

	measure2admins = {}
	for measure, admin in measure_admins:
		if measure.id not in measure2admins:
			measure2admins[measure.id] = {'measure': measure.to_small_dict(), 'hasTreat': False, 'hasControl': False}


		measure2admins[measure.id]['hasTreat'] = measure2admins[measure.id]['hasTreat'] or admin.treatment == treatment_id
		measure2admins[measure.id]['hasControl'] = measure2admins[measure.id]['hasControl'] or admin.treatment == 2182 


	measures = [measure['measure'] for measure in measure2admins.values() if measure['hasTreat'] and measure['hasControl']]

	has_next_token = (((page - 1) * ROWS_PER_PAGE) + ROWS_PER_PAGE) < len(measures)

	return ([], page, 0) if not measures else (measures[(page - 1) * ROWS_PER_PAGE : (((page - 1) * ROWS_PER_PAGE) + ROWS_PER_PAGE)], page+1 if has_next_token else None, len(measures))


def get_condition_scoring(treatment_name):
	treatment_query = db.session.query(Treatment).filter_by(name = treatment_name).subquery()
	codntion_scores = db.session.query(ConditionScore, Condition).join(treatment_query, ConditionScore.treatment == treatment_query.c.id)\
		.join(Condition, Condition.id == ConditionScore.condition).all()

	return codntion_scores
