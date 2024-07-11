from aws_cdk import (
    aws_lambda as _lambda,

    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct

class BasicAuthorizerStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, env_app: dict, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.basic_authorizer_lambda = _lambda.Function(
            self,
            id="BasicAuthorizerLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            code=_lambda.Code.from_asset("authorization_service/lambda_functions"),
            handler="basic_authorizer.lambda_handler",
            environment=env_app
        )
        
