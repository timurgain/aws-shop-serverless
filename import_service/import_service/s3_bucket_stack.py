import logging
from aws_cdk import (
    Stack,
    RemovalPolicy,
    aws_s3 as s3,
)
from constructs import Construct

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class S3BucketStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        try:
            # 0. Define CORS rules
            
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

            # 1. Create S3 Bucket

            self.bucket = s3.Bucket(
                self,
                id="TMShopImportServiceBucket",
                bucket_name="tm-shop-import-service-bucket",
                removal_policy=RemovalPolicy.DESTROY,
                cors=cors_rules,                
            )

            logger.info("S3BucketStack created successfully")    

        except Exception as err:
            logger.error(f"Error in S3BucketStack: {err}")
