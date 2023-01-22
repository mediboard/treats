from app import db, gpt_vectors
from app.models import Condition, StudyCondition, Baseline, baseline_type, \
  Treatment, StudyTreatment, Analytics, Measure, measure_type, Study, MeasureGroup, MeasureGroupMeasure, \
  ConditionGroup

def search_measures_by_vector(vector):
  response = gpt_vectors.query(
    vector=vector,
    top_k=20,
    include_values=False)

  measures = get_measures([int(x['id']) for x in response['matches']])

  id_2_score = {x['id']:x['score'] for x in response['matches']}

  return [(measure, id_2_score[str(measure.id)]) for measure in measures]


def get_measures(measure_ids):
  query = db.session.query(Measure)\
    .filter(Measure.id.in_(measure_ids))

  results = query.all()

  return results
