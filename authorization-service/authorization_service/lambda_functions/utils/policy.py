def generate_authorizer_policy(principal_id, effect, arn_resource):
    """Generate a policy document for the AWS API Gateway authorizer"""
    auth_response = {}
    auth_response['principalId'] = principal_id
    if effect and arn_resource:
        policy_document = {
            'Version': '2012-10-17',
            'Statement': [{
                'Action': 'execute-api:Invoke',
                'Effect': effect,
                'Resource': arn_resource
            }]
        }
        auth_response['policyDocument'] = policy_document
    return auth_response
