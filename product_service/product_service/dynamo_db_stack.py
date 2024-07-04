import logging
from aws_cdk import Stack, RemovalPolicy, aws_dynamodb as db
from constructs import Construct

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DynamoDBStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        try:
            self.products_table = db.Table(
                self,
                id="products",
                partition_key=db.Attribute(name="id", type=db.AttributeType.STRING),
                billing_mode=db.BillingMode.PROVISIONED,
                removal_policy=RemovalPolicy.DESTROY,
                read_capacity=5,
                write_capacity=5,
            )

            self.stocks_table = db.Table(
                self,
                id="stocks",
                partition_key=db.Attribute(
                    name="product_id", type=db.AttributeType.STRING
                ),
                billing_mode=db.BillingMode.PROVISIONED,
                removal_policy=RemovalPolicy.DESTROY,
                read_capacity=5,
                write_capacity=5,
            )
            logger.info("DynamoDBStack created successfully")

        except Exception as err:
            logger.error(f"Error in DynamoDBStack: {err}")
