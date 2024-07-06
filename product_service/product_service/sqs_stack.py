import logging
from aws_cdk import aws_sqs as sqs, aws_iam as iam, Stack
from constructs import Construct

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SQSStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        try:

            # 0. Create SQS queue

            self.catalog_items_queue = sqs.Queue(
                self,
                "CatalogItemsQueue",
                queue_name="catalog_items_queue",  # The queue name is used (hardcoded) in ImportShopProductsFileStack in import_service app
            )

            logger.info("SQS queue created successfully!")

        except Exception as e:
            logger.error(f"Error in SQSStack: {e}")
        