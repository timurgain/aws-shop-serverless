import logging
from aws_cdk import aws_sns as sns, aws_sns_subscriptions as sns_subscr, Stack
from constructs import Construct

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SNSTopicStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        try:
            # 0. Create SNS Topic

            self.create_product_topic = sns.Topic(
                self, "CreateProductTopic",
                topic_name="createProductTopic"
            )

            # 1. Email subscription with filter policy by price

            self.create_product_topic.add_subscription(
                sns_subscr.EmailSubscription(
                    "timur.gain@gmail.com",
                    filter_policy={
                        "price": sns.SubscriptionFilter.numeric_filter(
                            less_than=100
                        )
                    }
                )
            )

            self.create_product_topic.add_subscription(
                sns_subscr.EmailSubscription(
                    "timur.gain@yandex.ru",
                    filter_policy={
                        "price": sns.SubscriptionFilter.numeric_filter(
                            greater_than_or_equal_to=100
                        )
                    }
                )
            )

            logger.info("SNS Topic created successfully!")
        
        except Exception as e:
            logger.error(f"Error in SNSTopicStack: {e}")
