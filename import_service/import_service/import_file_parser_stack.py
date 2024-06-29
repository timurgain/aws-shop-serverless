import logging
from aws_cdk import (
    Stack,
    aws_iam as iam,
    aws_lambda as _lambda,
)
from constructs import Construct

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImportFileParserStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, s3_bucket_stack: Stack, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

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
                    actions=["s3:GetObject", "s3:PutObject", "s3:DeleteObject"],
                    resources=[f"{s3_bucket_stack.bucket.bucket_arn}/*"],
                )
            )

            # 2. Create lambda stack

            self.import_file_parser = _lambda.Function(
                self,
                id="ImportFileParser",
                runtime=_lambda.Runtime.PYTHON_3_11,
                code=_lambda.Code.from_asset("import_service/lambda_functions"),
                handler="import_file_parser.lambda_handler",
                role=lambda_role,
                environment={
                    "BUCKET_NAME": s3_bucket_stack.bucket.bucket_name,
                },
            )

            logger.info("ImportFileParserStack created successfully")

        except Exception as err:
            logger.error(f"Error in ImportFileParserStack: {err}")
