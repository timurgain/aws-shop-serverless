import json
import http
from utils.serializers import DecimalEncoder
from utils.constants import headers_safe_methods
from utils.managers import join_product_stock
from utils.dynamodb import initialize_dynamodb_tables
from utils.logging import log_request, log_info
from utils.errors import NotFoundError


def lambda_handler(event, context):
    """Iterate SQS messages that contain product data, process them, and create products and stocks in DynamoDB."""
    log_request(event)

    try:
        for message in event.get('Records', []):
            message_body = json.loads(message['body'])
            log_info(f"Message body: {message_body}") 

    except Exception as err:
        log_info(f"Error in catalog_batch_process: {err}")
