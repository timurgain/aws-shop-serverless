import base64
import os
from utils.policy import generate_authorizer_policy


def lambda_handler(event, context):
    """Authorizer function for API Gateway"""
    
    # 0. Get and decode the basic authorization token

    token = event['authorizationToken'].split(' ')[1]  # 'Basic token-value'
    username, password = base64.b64decode(token).decode('utf-8').split(':')

    # 1. Verify the username and password (for simplicity, values from .env are used)

    expected_username = os.getenv('GITHUB_ACCOUNT_LOGIN')
    expected_password = os.getenv('TEST_PASSWORD')

    if username == expected_username and password == expected_password:
        return generate_authorizer_policy(username, 'Allow', event['methodArn'])
    else:
        return generate_authorizer_policy(username, 'Deny', event['methodArn'])