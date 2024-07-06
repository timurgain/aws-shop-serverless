from aws_cdk import aws_sqs as sqs, aws_iam as iam, Stack
from constructs import Construct


class SQSStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # 0. Create SQS queue

        self.catalog_items_queue = sqs.Queue(
            self,
            "CatalogItemsQueue",
            queue_name="catalog_items_queue",  # The queue name is used (hardcoded) in ImportShopProductsFileStack in import_service app
        )
        