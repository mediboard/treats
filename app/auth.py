from flask_httpauth import HTTPTokenAuth 
from app import cognito_client
from app.errors import create_error


token_auth = HTTPTokenAuth()

@token_auth.verify_token
def verify_token(token):
    try:
        username = token.split('_', 1)[0]
        user = cognito_client.admin_get_user(UserPoolId='us-west-2_QduzpPLXm', Username=username)
        cognito_api_key = [x['Value'] for x in user['UserAttributes'] if x['Name'] == 'custom:apikey'][0]

        return token if cognito_api_key == token else None

    except:
        return None


@token_auth.error_handler
def basic_auth_error(status):
    return create_error(status)
