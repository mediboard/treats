import stripe

from flask_cors import cross_origin
from flask import request

from app import cognito_client
from app.api import bp, controller
from app.auth import token_auth
from app.errors import create_notfound_error

from app.treatments.controllers import treatments as treats_controller
from app.studies import controller as studies_controller
from app.measures import controller as measures_controller


'''
API routes
'''
@bp.route('/treatments/search')
@cross_origin(supports_credentials=True)
@token_auth.login_required
def search_treatments():
    query = request.args.get('q', '', type=str)
    limit = request.args.get('limit')
    results = treats_controller.search_treatments(query, limit or 5)

    return {'results': [x.to_dict() for x in results]}


@bp.route('/treatments/<int:treatment_id>/scan')
@cross_origin(supports_credentials=True)
@token_auth.login_required
def scan_treatments(treatment_id):
    results = treats_controller.get_treatment_diffs(treatment_id)

    return results


@bp.route('/treatments/<string:name>/effects')
@cross_origin(supports_credentials=True)
@token_auth.login_required
def get_treatment_effects(name):
    limit = int(request.args.get('limit'))
    effects = treats_controller.get_effects(name, limit, request.args)

    return {'effects': [{'name': name, 'no_effected': effected, 'no_at_risk': at_risk, 'no_studies': count, 'studies': studies} for name, effected, at_risk, count, studies in effects]}


@bp.route('/studies/search')
@cross_origin(supports_credentials=True)
@token_auth.login_required
def search_studies():
    limit = int(request.args.get('limit') or '10')
    studies, next_page, total = studies_controller.get_studies(
            request.args,
            int(request.args.get('page')),
            limit=limit)

    return {'studies': [study.to_summary_dict() for study in studies], 'next': next_page, 'total': total}


@bp.route('/studies/data')
@cross_origin(supports_credentials=True)
@token_auth.login_required
def search_studies():
    limit = int(request.args.get('limit') or '10')
    studies, next_page, total = studies_controller.get_studies(
            request.args,
            int(request.args.get('page')),
            limit=limit)

    return {'studies': [study.to_summary_dict() for study in studies], 'next': next_page, 'total': total}


@bp.route('/studies/<string:study_id>')
@cross_origin(supports_credentials=True)
@token_auth.login_required
def get_study(study_id):
    studies = studies_controller.get_study(study_id)
    if (not studies):
        return create_notfound_error('Study with id {0} not found'.format(study_id))
        
    return {'studies': [study.to_summary_dict() for study in studies]}


@bp.route('/measures/search')
@cross_origin(supports_credentials=True)
@token_auth.login_required
def search_measures():
  query = request.args.get('q')
  q_vector = get_embedding(query)
  results = controller.search_measures_by_vector(q_vector)

  return {'measures': [{**x[0].to_small_dict(), 'score': x[1]} for x in results]}


'''
API setup and configuration
'''
@bp.route('/config')
@cross_origin(supports_credentials=True)
def get_publishable_key():
    key = os.environ.get('STRIPE_PUBLISHABLE_KEY') or 'pk_test_51LNmVkGBePS6GBskaippxoOPE9a6umnQBMmzjDJaONEn4POuf9lMoV68tHMF8XESvbmEYUVc2aHsa1IhuoWs1G2x00uyPRqCdC'

    return { "publicKey": key }


@bp.route('/checkout')
@cross_origin(supports_credentials=True)
def create_api_checkout():
    session = controller.create_api_checkout_session()

    return { "session": session }


@bp.route('/session/<string:session_id>')
@cross_origin(supports_credentials=True)
def get_session(session_id):
    session = controller.fetch_checkout_session(session_id)

    return { "session": session }


@bp.route('/<string:username>/stripeid/<string:stripe_id>/token')
@cross_origin(supports_credentials=True)
def create_api_token(username, stripe_id):
    new_token = controller.new_api_key(username, stripe_id)

    return { 'token': new_token }
