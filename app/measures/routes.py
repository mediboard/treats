from app.errors import create_notfound_error
from app.measures import bp
from flask_cors import cross_origin
from app.measures import controller
from flask import request
from app.utils import calculate_results_summary, get_embedding


@bp.route('/')
@cross_origin(supports_credentials=True)
def main():
  return 'Hello World'


@bp.route('/search')
@cross_origin(supports_credentials=True)
def search_measures_by_vector():
  query = request.args.get('q')

  q_vector = get_embedding(query)

  results = controller.search_measures_by_vector(q_vector)

  return {'measures': [{**x[0].to_small_dict(), 'score': x[1]} for x in results]}
