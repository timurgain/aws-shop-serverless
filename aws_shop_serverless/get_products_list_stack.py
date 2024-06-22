from aws_cdk import (
    Stack,
    aws_iam as iam,
    aws_lambda as _lambda,
)
from constructs import Construct


class GetProductsListStack(Stack):

    def __init__(
        self, scope: Construct, construct_id: str, dynamodb_stack: Stack, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 0. Create the IAM role

        lambda_role = iam.Role(
            self,
            "LambdaExecutionRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
        )

        # 1. Attach the policy to the role

        lambda_role.add_to_policy(
            iam.PolicyStatement(
                actions=["dynamodb:Scan", "dynamodb:GetItem", "dynamodb:Query"],
                resources=[
                    dynamodb_stack.products_table.table_arn,
                    dynamodb_stack.stocks_table.table_arn,
                ],
            )
        )

        # 2. Create lambda stack

        self.get_products = _lambda.Function(
            self,
            id="GetProductsList",
            runtime=_lambda.Runtime.PYTHON_3_11,
            code=_lambda.Code.from_asset("aws_shop_serverless/lambda_functions"),
            handler="get_products_list.lambda_handler",
            role=lambda_role,
            environment={
                "PRODUCTS_TABLE_NAME": dynamodb_stack.products_table.table_name,
                "STOCKS_TABLE_NAME": dynamodb_stack.stocks_table.table_name,
            },
        )
