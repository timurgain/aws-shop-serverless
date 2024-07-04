import json
import http
import uuid
from decimal import Decimal
from utils.constants import headers_mutating_methods
from utils.dynamodb import get_products_table_name, get_stocks_table_name, execute_transact_write
from utils.managers import join_product_stock
from utils.logging import log_request
from utils.errors import BadRequestError


def lambda_handler(event, context):
    """Create product Lambda function handler."""
    log_request(event)

    try:
        # 1. Read request body

        try:
            body = json.loads(event.get("body", "{}"))
        except json.JSONDecodeError as e:
            raise BadRequestError(f"Invalid JSON payload: {str(e)}")
        
        product_id = str(uuid.uuid4())
        title = body.get("title")
        description = body.get("description")
        price = body.get("price")
        count = body.get("count", 0)

        if not title or not description or not price:
            raise BadRequestError("Invalid request body: title, description and price are required")
        
        if not isinstance(price, (int, float, Decimal)) or not price > 0:
            raise BadRequestError("Invalid request body: price should be a positive number")
        
        if not isinstance(count, int) or not count >= 0:
            raise BadRequestError("Invalid request body: count should be an integer that is greater or equal to 0")

        # 2. Prepare product data and stock data for DynamoDB TransactWriteItems operation

        product = {
            'Put': {
                "TableName": get_products_table_name(),
                "Item": {
                    "id": {"S": product_id},
                    "title": {"S": title},
                    "description": {"S": description},
                    "price": {"N": str(price)},
                }
            }
        }

        stock = {
            'Put': {
                "TableName": get_stocks_table_name(),
                "Item": {
                    "product_id": {"S": product_id},
                    "count": {"N": str(count)},
                }
            }
        }

        # 3. Put product and stock data into DynamoDB using TransactWriteItems operation
        
        execute_transact_write([product, stock])

        # 4. Response

        joined_product_data = {
            "id": product_id,
            "title": title,
            "description": description,
            "price": str(price),
            "count": str(count),
        }

        return {
            "headers": headers_mutating_methods,
            "statusCode": http.HTTPStatus.CREATED,
            "body": json.dumps(joined_product_data),
        }
        
    except BadRequestError as err:
        return {
            "headers": headers_mutating_methods,
            "statusCode": http.HTTPStatus.BAD_REQUEST,
            "body": json.dumps({"error": str(err)}),
        }
    
    except Exception as err:
        return {
            "headers": headers_mutating_methods,
            "statusCode": http.HTTPStatus.INTERNAL_SERVER_ERROR,
            "body": json.dumps({"error": str(err)}),
        }
