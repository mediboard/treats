import stripe
import app

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
