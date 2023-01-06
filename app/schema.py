import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from graphene_sqlalchemy_filter import FilterableConnectionField, FilterSet
import app.models as models

#
# FILTERS
#
class StudyFilters(FilterSet):
	class Meta:
		model = models.Study
		fields = {
			'upload_date': [...],
			'short_title': [...],
			'official_title': [...],
			'description': [...],
			'responsible_party': [...],
			'sponsor': [...],
			'type': [...],
			'purpose': [...],
			'intervention_type': [...],
			'min_age': [...],
			'min_age_units': [...],
			'max_age': [...],
			'max_age_units': [...],
			'gender': [...],
			'results_summary': [...]
		}


class ConditionGroupFilters(FilterSet):
	class Meta:
		model = models.ConditionGroup
		fields = {
			'name': [...]
		}


# For some reason you can't filter this nested in studies
class ConditionFilters(FilterSet):
	class Meta:
		model = models.Condition
		fields = {
			'name': [...],
		}


class MeasureGroupFilters(FilterSet):
	class Meta:
		model = models.MeasureGroup
		fields = {
			'name': [...],
			'type': [...]
		}


class MeasureFilters(FilterSet):
	class Meta:
		model = models.Measure
		fields = {
			'title': [...],
			'description': [...],
			'dispersion': [...],
			'type': [...],
			'param': [...],
			'units': [...]
		}


class TreatmentFilters(FilterSet):
	class Meta: 
		model = models.Treatment
		fields = {
			'name': [...],
			'from_study': [...],
			'no_studies': [...],
		}


class GroupFilters(FilterSet):
	class Meta:
		model = models.Group
		fields = {
			'title': [...],
			'study_id': [...],
			'description': [...],
		}


class OutcomeFilters(FilterSet):
	class Meta:
		model = models.Outcome
		fields = {
			'title': [...],
			'value': [...],
			'dispersion': [...],
			'upper': [...],
			'lower': [...],
			'no_participants': [...]
		}


class AdministrationFilters(FilterSet):
	class Meta:
		model = models.Administration
		fields = {
			'description': [...]
		}


class AnalyticsFilters(FilterSet):
	class Meta:
		model = models.Analytics
		fields = {
			'from_study': [...],
			'method': [...],
			'p_value': [...],
			'param_type': [...],
			'is_non_inferiority': [...],
			'non_inferiority_type': [...],
			'non_inferiority_comment': [...],
			'param_value': [...],
			'ci_pct': [...],
			'ci_lower': [...],
			'ci_upper': [...]
		}


class BaselineFilters(FilterSet):
	class Meta:
		model = models.Baseline
		fields = {
			'base': [...],
			'clss': [...],
			'category': [...],
			'param_type': [...],
			'dispersion': [...],
			'unit': [...],
			'value': [...],
			'spread': [...],
			'upper': [...],
			'lower': [...],
			'type': [...],
			'sub_type': [...],
		}


class EffectFilters(FilterSet):
	class Meta:
		model = models.Effect
		fields = {
			'name': [...],
			'organ_system': [...],
			'effect_type': [...],
			'assessment': [...],
			'no_effected': [...],
			'no_at_risk': [...],
			'collection_threshold': [...]
		}


class EffectGroupFilters(FilterSet):
	class Meta:
		model = models.EffectGroup
		fields = {
			'title': [...],
			'description': [...],
			'study_id': [...]
		}


class CustomField(FilterableConnectionField):
	filters = {
		models.Study: StudyFilters(),
		models.Measure: MeasureFilters(),
		models.Condition: ConditionFilters(),
		models.Treatment: TreatmentFilters(),
		models.Group: GroupFilters(),
		models.Outcome: OutcomeFilters(),
		models.Administration: AdministrationFilters(),
		models.Analytics: AnalyticsFilters(),
		models.Baseline: BaselineFilters(),
		models.Effect: EffectFilters(),
		models.EffectGroup: EffectGroupFilters()
	}

#
# NODES
#

class EffectGroup(SQLAlchemyObjectType):
	class Meta:
		model = models.EffectGroup
		interfaces = (graphene.relay.Node, )
		connection_field_factory = CustomField.factory


class Effect(SQLAlchemyObjectType):
	class Meta:
		model = models.Effect
		interfaces = (graphene.relay.Node, )
		connection_field_factory = CustomField.factory


class Baseline(SQLAlchemyObjectType):
	class Meta:
		model = models.Baseline
		interfaces = (graphene.relay.Node, )
		connection_field_factory = CustomField.factory


class Analytics(SQLAlchemyObjectType):
	class Meta:
		model = models.Analytics 
		interfaces = (graphene.relay.Node, )
		connection_field_factory = CustomField.factory


class Administration(SQLAlchemyObjectType):
	class Meta:
		model = models.Outcome 
		interfaces = (graphene.relay.Node, )
		connection_field_factory = CustomField.factory


class Outcome(SQLAlchemyObjectType):
	class Meta:
		model = models.Outcome 
		interfaces = (graphene.relay.Node, )
		connection_field_factory = CustomField.factory


class Group(SQLAlchemyObjectType):
	class Meta:
		model = models.Group 
		interfaces = (graphene.relay.Node, )
		connection_field_factory = CustomField.factory


class Condition(SQLAlchemyObjectType):
	class Meta:
		model = models.Condition 
		interfaces = (graphene.relay.Node, )
		connection_field_factory = CustomField.factory


class Treatment(SQLAlchemyObjectType):
	class Meta:
		model = models.Treatment
		interfaces = (graphene.relay.Node, )
		connection_field_factory = CustomField.factory


class Measure(SQLAlchemyObjectType):
	class Meta:
		model = models.Measure
		interfaces = (graphene.relay.Node, )
		connection_field_factory = CustomField.factory


class Study(SQLAlchemyObjectType):
	class Meta:
		model = models.Study 
		interfaces = (graphene.relay.Node, )
		connection_field_factory = CustomField.factory


class Query(graphene.ObjectType):
	node = graphene.relay.Node.Field()

	all_studies = CustomField(Study.connection) 
	all_measures = CustomField(Measure.connection) 
	all_conditions = CustomField(Condition.connection)
	all_treatments = CustomField(Treatment.connection)
	all_groups = CustomField(Group.connection)
	all_outcomes = CustomField(Outcome.connection)
	all_administrations = CustomField(Administration.connection)
	all_analytics = CustomField(Analytics.connection)
	all_baselines = CustomField(Baseline.connection)
	all_effects = CustomField(Effect.connection)
	all_effect_groups = CustomField(EffectGroup.connection)
