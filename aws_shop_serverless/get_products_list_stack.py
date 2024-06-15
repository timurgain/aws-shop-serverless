from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
)
from constructs import Construct


class GetProductsListStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.get_products = _lambda.Function(
            self,
            id="GetProductsList",
            runtime=_lambda.Runtime.PYTHON_3_11,
            code=_lambda.Code.from_asset("aws_shop_serverless/lambda_functions"),
            handler="get_products_list.lambda_handler",
        )
