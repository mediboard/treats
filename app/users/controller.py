import stripe
import os
import base64

from app import cognito_client 


def create_api_checkout_session():
    client_url = os.environ.get('CLIENT_BASE_URL') or 'http://localhost:3000'
    checkout_session = stripe.checkout.Session.create(
        success_url=client_url + "/users/success?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=client_url + "/cancelled",
        payment_method_types=["card", "us_bank_account"],
        mode="subscription",
        line_items=[
            {
                "price": 'price_1MYZNYGBePS6GBskF7alD0U3',
                "quantity": 1,
            }
        ]
    )

    return checkout_session


def fetch_checkout_session(session_id):
    return stripe.checkout.Session.retrieve(session_id)


def new_api_key(username, stripe_id):
    user = cognito_client.admin_get_user(UserPoolId='us-west-2_QduzpPLXm', Username=username)
    cognito_stripe_id = user['UserAttributes'].filter(lambda x: x['Name'] == 'custom:stripeId')[0]['Value']
    if (stripe_id == cognito_stripe_id):
        return base64.b64encode(os.urandom(24)).decode('utf-8')

    return None
