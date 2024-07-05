from aws_cdk import (aws_sqs as sqs, Stack)
from constructs import Construct


class SQSStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        self.catalog_items_queue = sqs.Queue(
            self, "CatalogItemsQueue",
            queue_name="catalog_items_queue"
        )
