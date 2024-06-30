import logging
from aws_cdk import (
    Stack,
    aws_iam as iam,
    aws_lambda as _lambda,
)
from constructs import Construct

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GetProductByIdStack(Stack):

    def __init__(
        self, scope: Construct, construct_id: str, dynamodb_stack: Stack, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        if not dynamodb_stack:
            raise ValueError("dynamodb_stack is required")

        try:

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

            self.get_product_by_id = _lambda.Function(
                self,
                id="GetProductById",
                runtime=_lambda.Runtime.PYTHON_3_11,
                code=_lambda.Code.from_asset("product_service/lambda_functions"),
                handler="get_product_by_id.lambda_handler",
                role=lambda_role,
                environment={
                    "PRODUCTS_TABLE_NAME": dynamodb_stack.products_table.table_name,
                    "STOCKS_TABLE_NAME": dynamodb_stack.stocks_table.table_name,
                },
            )

            logger.info("GetProductByIdStack created successfully")

        except Exception as err:
            logger.error(f"Error in GetProductByIdStack: {err}")
