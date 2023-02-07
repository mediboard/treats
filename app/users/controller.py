import stripe
import os


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
