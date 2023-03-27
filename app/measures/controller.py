from app import db, gpt_vectors
from sqlalchemy.orm import joinedload, raiseload
from sqlalchemy import func, distinct, desc, or_, and_, text, case, literal_column
from app.models import Condition, StudyCondition, Baseline, baseline_type, \
  Treatment, StudyTreatment, Analytics, Measure, measure_type, Study, MeasureGroup, MeasureGroupMeasure, \
  ConditionGroup, Group, Administration

def search_measures_by_vector(vector):
  response = gpt_vectors.query(
    vector=vector,
    top_k=20,
    include_values=False)

  measures = get_measures([int(x['id']) for x in response['matches']])

  id_2_score = {x['id']:x['score'] for x in response['matches']}

  return [(measure, id_2_score[str(measure.id)]) for measure in measures]


def get_measure_groups(treatment_ids, condition_id):
  single_groups = db.session.query(Group, func.count(Administration.id))\
    .join(Administration, Administration.group == Group.id)\
    .group_by(Group.id)\
    .having(func.count(Administration.id) <= 3)\
    .subquery()

  measure_groups = db.session.query(MeasureGroup)\
    .join(MeasureGroupMeasure, MeasureGroupMeasure.measureGroup == MeasureGroup.id)\
    .join(Measure, Measure.id == MeasureGroupMeasure.measure)\
    .join(single_groups, single_groups.c.study == Measure.study)\
    .join(Administration, Administration.group == single_groups.c.id)\
    .join(StudyCondition, StudyCondition.study == Measure.study)\
    .filter(StudyCondition.condition == condition_id)\
    .filter(or_(*[Administration.treatment==treat for treat in treatment_ids]))\
    .all()

  return measure_groups


def get_measures(measure_ids):
  query = db.session.query(Measure)\
    .filter(Measure.id.in_(measure_ids))

  results = query.all()

  return results


def get_data(measure_id):
  measure_data = db.session.query(Measure)\
    .filter(Measure.id == measure_id)\
    .options(
      joinedload(Measure.outcomes),
      joinedload(Measure.analytics).joinedload(Analytics.groups),
      raiseload('*'))\
    .first()

  groups = db.session.query(Group)\
    .join(Measure, Measure.study == Group.study)\
    .filter(Measure.id == measure_id)\
    .options(
      joinedload(Group.treatments),
      raiseload('*')
    )\
    .all()

  return measure_data, groups

