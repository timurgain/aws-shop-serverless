import json
import uuid
from utils.dynamodb import execute_transact_write, prepare_product_stock_data
from utils.logging import log_request, log_info


def lambda_handler(event, context):
    """Iterate SQS messages that contain product data, process them, and create products and stocks in DynamoDB."""
    log_request(event)

    try:
        for message in event.get("Records", []):

            # 1. Loop through SQS messages

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

    except Exception as err:
        log_info(f"Error in catalog_batch_process: {err}")
