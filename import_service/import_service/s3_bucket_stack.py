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
            # 0. Create S3 Bucket
            bucket = s3.Bucket(
                self,
                id="TMShopImportServiceBucket",
                bucket_name="tm-shop-import-service-bucket",
                removal_policy=RemovalPolicy.DESTROY,
            )          

        except Exception as err:
            logger.error(f"Error in S3BucketStack: {err}")
