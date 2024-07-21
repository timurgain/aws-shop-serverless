import logging
from aws_cdk import (
    CfnOutput,
    Fn,
    aws_lambda as _lambda,
    aws_iam as iam,
    Stack,
)
from constructs import Construct

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BasicAuthorizerStack(Stack):

    def __init__(
        self, scope: Construct, construct_id: str, env_app: dict, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        try:
            # 0. Import environment variables

            # 1. Create a lambda function for the basic authorizer

            self.basic_authorizer_lambda = _lambda.Function(
                self,
                id="BasicAuthorizerLambda",
                runtime=_lambda.Runtime.PYTHON_3_11,
                code=_lambda.Code.from_asset("authorization_service/lambda_functions"),
                handler="basic_authorizer.lambda_handler",
                environment=env_app,
            )

            # 2. Add permission for API Gateway to invoke the Lambda function

            self.basic_authorizer_lambda.add_permission(
                id="APIGatewayInvoke",
                principal=iam.ServicePrincipal("apigateway.amazonaws.com"),
                action="lambda:InvokeFunction",
            )

            # 3. Export the lambda function ARN for other stacks

            CfnOutput(
                self,
                id="BasicAuthorizerLambdaArn",
                value=self.basic_authorizer_lambda.function_arn,
                export_name="BasicAuthorizerLambdaArn",
            )

            logger.info("BasicAuthorizerStack created successfully")

        except Exception as err:
            logger.error(f"Error in BasicAuthorizerStack: {err}")
