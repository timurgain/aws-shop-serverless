import json
import http
import uuid
from utils.constants import headers_mutating_methods
from utils.dynamodb import (
    execute_transact_write,
    prepare_product_stock_data,
)

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

        # 2. Prepare product and stock

        product, stock = prepare_product_stock_data(
            product_id, title, description, price, count
        )

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
