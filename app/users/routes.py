import stripe
from app import cognito_client

from app.users import bp, controller
from flask_cors import cross_origin
from flask import request


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
