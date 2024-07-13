import logging
from typing import List, Tuple
from aws_cdk import (
    CfnOutput,
    Fn,
    Stack,
    aws_apigateway as apigateway,
    aws_lambda as _lambda,
)
from constructs import Construct

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class APIGatewayImportFileStack(Stack):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        method_url_lambdas: List[Tuple[str, str, _lambda.Function]],
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        try:
            # 0. Import the lambda authorizer ARN and reference it

            lambda_authorizer_arn = Fn.import_value("BasicAuthorizerLambdaArn")
            lambda_authorizer = _lambda.Function.from_function_arn(
                self, id="BasicAuthorizerLambda", function_arn=lambda_authorizer_arn
            )

            # 1. Create APIGateway

            default_lambda = method_url_lambdas[0][2]

            api = apigateway.LambdaRestApi(
                self,
                id="ImportAPI",
                rest_api_name="Import API",
                handler=default_lambda,
            )

            # 2. Create authorizer

            authorizer = apigateway.TokenAuthorizer(
                self,
                id="Authorizer",
                handler=lambda_authorizer,
                identity_source=apigateway.IdentitySource.header("Authorization"),
            )

            # 3. Bind http methods with lamdas within APIGateway

            resources = {}
            for methods, url, lambda_function in method_url_lambdas:
                parts = url.split("/")  # ['products','{product_id}']

                for i in range(len(parts)):
                    path = "/".join(parts[: i + 1])
                    if path not in resources:
                        parent_path = "/".join(parts[:i])
                        parent_resource = resources.get(parent_path, api.root)
                        resources[path] = parent_resource.add_resource(parts[i])

                resource = resources[url]

                for method in methods:
                    resource.add_method(
                        method,
                        integration=apigateway.LambdaIntegration(lambda_function),
                        authorizer=authorizer,
                    )

            # 4. Export the API Gateway ARN for other stacks
            
            # CfnOutput(
            #     self,
            #     id="APIGatewayImportArn",
            #     value=f"arn:aws:apigateway:{self.region}::/restapis/{api.rest_api_id}",
            #     export_name="APIGatewayImportArn",
            # )
            
            logger.info("APIGatewayImportFileStack created successfully")

        except Exception as err:
            logger.error(f"Error in APIGatewayImportFileStack: {err}")
