from app.studies.data import bp, controller
from app import db
from flask_cors import cross_origin
from flask import request
from app.errors import create_notfound_error


@bp.route('/')
@cross_origin(supports_credentials=True)
def main():
  return "Hello World"


AGG_ATTRIBUTES = [
  'sponsor',
  'responsible_party',
  'type',
  'purpose',
  'intervention_type',
  'phase',
  'completion_date',
  'status'
]

@bp.route('/<string:attr>')
@cross_origin(supports_credentials=True)
def agg_attr(attr):
  # if attr not in AGG_ATTRIBUTES:
  #   return create_notfound_error(f"{attr} not aggregateable")

  from app.studies import controller as study_controller
  study_query = study_controller.get_studies(request.args, subquery=True)

  attr_counts = None
  if (attr == 'treatments'):
    attr_counts = controller.agg_treatments(study_query, limit=request.args.get('limit', 10))

  elif (attr == 'conditions'):
    attr_counts = controller.agg_conditions(study_query, limit=request.args.get('limit', 10))

  elif (attr == 'baselines'):
    attr_counts = controller.agg_baselines(study_query, limit=request.args.get('limit', 10))

  else: 
    attr_counts = controller.query_attr(attr, study_query, limit=request.args.get('limit', 10))

  return_dict = {}
  counts = {}
  for name, count in attr_counts:
    name_str = str(name)

    if name_str not in counts:
      counts[name_str] = 0

    counts[name_str] += count

  return_dict[attr] = counts

  return return_dict


