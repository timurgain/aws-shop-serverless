import logging
from typing import List, Tuple
from aws_cdk import (
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
            default_lambda = method_url_lambdas[0][2]

            # 1. Create APIGateway

            api = apigateway.LambdaRestApi(
                self,
                id="ImportAPI",
                rest_api_name="Import API",
                handler=default_lambda,
            )

            # 2. Bind http methods with lamdas within APIGateway

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
                        method, integration=apigateway.LambdaIntegration(lambda_function)
                    )

            logger.info("APIGatewayImportFileStack created successfully")

        except Exception as err:
            logger.error(f"Error in APIGatewayImportFileStack: {err}")
