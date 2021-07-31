from app.treatments.models import Baseline, Treatment, Administration, Study, Group,\
	Effect, EffectGroup, EffectAdministration, Condition, StudyCondition, Comparison, Analytics
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
	# The basic idea is aggregating the analytics with this treatment in the group
	# We need to add in the concept of "mixed" and "direct" for a condition
	# Yes we should have a direct score and a mixed score 
	treatment_query = db.session.query(Treatment).filter_by(name = treatment_name).subquery()
	admin_query = db.session.query(Administration).join(treatment_query, Administration.treatment == treatment_query.c.id).subquery()
	group_query = db.session.query(Group).join(admin_query, Group.id == admin_query.c.group).subquery()
	comp_query = db.session.query(Comparison).join(group_query, Comparison.group == group_query.c.id).subquery()
	comp_alias = aliased(Comparison, comp_query)
	# Now get back the groups&treatments (or just the treatments)
	analytics_comps_treats = db.session.query(Analytics, comp_alias, Treatment)\
		.join(Group, Group.id == comp_alias.group)\
		.join(Administration, Administration.group == Group.id)\
		.join(Treatment, Treatment.id == Administration.treatment)\
		.join(Analytics, Analytics.id == comp_alias.analytic).all()

	# Create a structure for indexing
	id2analytic = {}
	id2comp = {}
	analytics_tree = {}
	for i in range(len(analytics_comps_treats)):
		curr_analytic = analytics_comps_treats[i][0]
		curr_comp = analytics_comps_treats[i][1]
		curr_treatment = analytics_comps_treats[i][2]

		if curr_analytic.id not in id2analytic:
			id2analytic[curr_analytic.id] = curr_analytic
		if curr_comp.id not in id2comp:
			id2comp[curr_comp.id] = curr_comp

		if curr_analytic.id not in analytics_tree:
			analytics_tree[curr_analytic.id] = {}
		if curr_comp.id not in analytics_tree[curr_analytic.id]:
			analytics_tree[curr_analytic.id][curr_comp.id] = []

		analytics_tree[curr_analytic.id][curr_comp.id].append(curr_treatment.name)

	# Remove analytics where the treatment is repeated in all the comps
	for analytic_id in analytics_tree.keys():
		bool_arr = [treatment_name in analytics_tree[comp] for comp in analytics_tree[analytic_id]]
		if (sum(bool_arr) == len(bool_arr)):
			del analytics_tree[analytic_id]

	# Split singular and mixed
	# singular_analytics = []
	# for analytic_id in analytics_tree.keys():
	# 	bool_arr = [!None not in analytics_tree[comp] and treatment_name not in analytics_tree[comp] for comp in analytics_tree[analytic_id]]
	# 	if (sum(bool_arr) == len(bool_arr)):
	# 		singular_analytics.append(analytic)

	mixed_analytics = [analytics_id for analytic_id in analytics_tree.keys() if analytic_id not in singular_analytics]

	return {}
