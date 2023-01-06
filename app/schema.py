import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from graphene_sqlalchemy_filter import FilterableConnectionField, FilterSet
import app.models as models


class StudyFilters(FilterSet):
	class Meta:
		model = models.Study
		fields = {
			'short_title': [...],
			'upload_date': [...],
			'min_age_units': [...]
		}


class MeasureFilters(FilterSet):
	class Meta:
		model = models.Measure
		fields = {
			'title': [...]
		}


class CustomField(FilterableConnectionField):
	filters = {
		models.Study: StudyFilters(),
		models.Measure: MeasureFilters()
	}


class Condition(SQLAlchemyObjectType):
	class Meta:
		model = models.Condition 
		interfaces = (graphene.relay.Node, )


class Treatment(SQLAlchemyObjectType):
	class Meta:
		model = models.Treatment
		interfaces = (graphene.relay.Node, )


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

	all_conditions = SQLAlchemyConnectionField(Condition.connection)
	all_treatments = SQLAlchemyConnectionField(Treatment.connection)






