import os
import json
import uuid
import boto3
from utils.dynamodb import execute_transact_write, prepare_product_stock_data
from utils.logging import log_request, log_info
# from product_service.product_service.lambda_functions.utils.dynamodb import execute_transact_write, prepare_product_stock_data
# from product_service.product_service.lambda_functions.utils.logging import log_request, log_info


sns_topic_arn = os.environ.get("SNS_TOPIC_ARN")
sns = boto3.client("sns")


def lambda_handler(event, context):
    """Iterate SQS messages that contain product data, process them, and create products and stocks in DynamoDB."""
    log_request(event)

    try:
        # 0. Loop through SQS messages

        messages = event.get("Records", [])
        for message in messages:

            # 1. Parse message body

            message_body = json.loads(message["body"])

            product_id = str(uuid.uuid4())
            title = message_body.get("title")
            description = message_body.get("description")
            price = int(message_body.get("price"))
            count = int(message_body.get("count", 0))

            # 2. Prepare product and stock

            product, stock = prepare_product_stock_data(
                product_id, title, description, price, count
            )

            # 3. Put product and stock data into DynamoDB using TransactWriteItems operation

            execute_transact_write([product, stock])

            # 4. Log the processed message

            log_info(f"Processed message: {message_body}")

            # 5. Publish message to SNS topic

            sns.publish(
                TopicArn=sns_topic_arn,
                Message=json.dumps(
                    {
                        "message": f"Catalog batch process completed successfully, created {title}, price: {price}."
                    }
                ),
                MessageAttributes={
                    "title": {"DataType": "String", "StringValue": title},
                    "price": {"DataType": "Number", "StringValue": str(price)},
                }
            )

    except Exception as err:
        log_info(f"Error in catalog_batch_process: {err}")

        sns.publish(
            TopicArn=sns_topic_arn,
            Message=json.dumps(
                {
                    "message": f"Catalog batch process failed: {str(err)}"
                }
            ),
        )
