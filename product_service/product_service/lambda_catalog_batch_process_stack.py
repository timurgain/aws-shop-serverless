import logging
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_lambda_event_sources as lambda_event_sources,
    aws_iam as iam,
)
from constructs import Construct

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LambdaCatalogBatchProcessStack(Stack):

    def __init__(
        self, scope: Construct, construct_id: str, dynamodb_stack, sqs_stack, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        try:
            # 1. Create lambda stack

            self.catalog_batch_process = _lambda.Function(
                self,
                id="CatalogBatchProcess",
                runtime=_lambda.Runtime.PYTHON_3_11,
                code=_lambda.Code.from_asset("product_service/lambda_functions"),
                handler="catalog_batch_process.lambda_handler",
                environment={
                    "PRODUCTS_TABLE_NAME": dynamodb_stack.products_table.table_name,
                    "STOCKS_TABLE_NAME": dynamodb_stack.stocks_table.table_name,
                    'SQS_QUEUE_NAME': 'catalog_items_queue'  # Hardcoded queue name from SQSStack that is created in an other app
                },
            )

            # 2. Event source for the lambda is SQS queue

            self.catalog_batch_process.add_event_source(
                lambda_event_sources.SqsEventSource(
                    queue=sqs_stack.catalog_items_queue,
                    batch_size=5
                )
            )

            # 3. SQS, grant consume permissions to the lambda

            sqs_stack.catalog_items_queue.grant_consume_messages(
                self.catalog_batch_process
            )

            # 3. DynamoDb, grant read/write permissions to the lambda

            dynamodb_stack.products_table.grant_read_write_data(
                self.catalog_batch_process
            )
            dynamodb_stack.stocks_table.grant_read_write_data(
                self.catalog_batch_process
            )

            logger.info("GetProductsListStack created successfully")

        except Exception as err:
            logger.error(f"Error in LambdaCatalogBatchProcessStack: {err}")
