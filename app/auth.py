from flask_httpauth import HTTPTokenAuth 
from app import cognito_client
from app.errors import create_error


basic_auth = HTTPBasicAuth()

@token_auth.verify_token
def verify_token(token):
    user = cognito_client.admin_get_user(UserPoolId='us-west-2_QduzpPLXm', Username=user_name)
    cognito_api_key = user['UserAttributes'].filter(lambda x: x['Name'] == 'custom:apikey')[0]['Value']
    
    return cognito_api_key == api_key


@token_auth.error_handler
def basic_auth_error(status):
    return create_error(status)