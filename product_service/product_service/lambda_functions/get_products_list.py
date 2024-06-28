import json
import http
from utils.serializers import DecimalEncoder
from utils.constants import headers_safe_methods
from utils.managers import join_product_stock
from utils.dynamodb import initialize_dynamodb_tables
from utils.logging import log_request


def lambda_handler(event, context):
    """Get products list Lambda function handler."""
    log_request(event)
    
    try:
        # 0. Init

        products_table, stocks_table = initialize_dynamodb_tables()

        # 1. Get all products and stocks

        products = products_table.scan().get("Items", [])
        stocks = stocks_table.scan().get("Items", [])
        joined_products_data = [
            join_product_stock(product, stocks) for product in products
        ]

        # 2. response

        return {
            "headers": headers_safe_methods,
            "statusCode": http.HTTPStatus.OK,
            "body": json.dumps(joined_products_data, cls=DecimalEncoder),
        }

    except Exception as err:
        return {
            "headers": headers_safe_methods,
            "statusCode": http.HTTPStatus.INTERNAL_SERVER_ERROR,
            "body": json.dumps(str(err)),
        }
