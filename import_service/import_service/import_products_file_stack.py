import logging
from aws_cdk import (
    Stack,
    aws_iam as iam,
    aws_lambda as _lambda,
    RemovalPolicy,
    aws_s3 as s3,
)
from constructs import Construct
from aws_cdk.aws_lambda_event_sources import S3EventSource


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImportShopProductsFileStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        try:
            # 0. Define roles and rules

            cors_rules = [
                s3.CorsRule(
                    allowed_methods=[
                        s3.HttpMethods.GET,
                        s3.HttpMethods.PUT,
                        s3.HttpMethods.POST,
                        s3.HttpMethods.DELETE,
                    ],
                    allowed_origins=["*"],
                    allowed_headers=["*"],
                    max_age=3000,
                )
            ]

            lambda_role = iam.Role(
                self,
                "LambdaExecutionRole",
                assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            )

            # 1. Create S3 Bucket

            self.bucket = s3.Bucket(
                self,
                id="ShopImportServiceBucket",
                bucket_name="tmshop-import-service-bucket",
                removal_policy=RemovalPolicy.DESTROY,
                cors=cors_rules,
            )

            # 2. Attach the policy to the role

            lambda_role.add_to_policy(
                iam.PolicyStatement(
                    actions=["s3:GetObject", "s3:PutObject", "s3:DeleteObject"],
                    resources=[f"{self.bucket.bucket_arn}/*"],
                )
            )

            # 3. Create lambdas

            self.import_products_file = _lambda.Function(
                self,
                id="ImportProductsFile",
                runtime=_lambda.Runtime.PYTHON_3_11,
                code=_lambda.Code.from_asset("import_service/lambda_functions"),
                handler="import_products_file.lambda_handler",
                role=lambda_role,
                environment={
                    "BUCKET_NAME": self.bucket.bucket_name,
                },
            )

            self.import_file_parser = _lambda.Function(
                self,
                id="ImportFileParser",
                runtime=_lambda.Runtime.PYTHON_3_11,
                code=_lambda.Code.from_asset("import_service/lambda_functions"),
                handler="import_file_parser.lambda_handler",
                role=lambda_role,
                environment={
                    "BUCKET_NAME": self.bucket.bucket_name,
                },
            )

            # 4. Add S3 event as trigger to the import_file_parser lambda

            self.import_file_parser.add_event_source(
                S3EventSource(
                    bucket=self.bucket,
                    events=[s3.EventType.OBJECT_CREATED],
                    filters=[s3.NotificationKeyFilter(prefix="uploaded/")],
                )
            )

            logger.info("ImportFileStack created successfully")

        except Exception as err:
            logger.error(f"Error in ImportFileStack: {err}")
