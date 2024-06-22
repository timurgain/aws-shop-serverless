import json
import http
import uuid
from decimal import Decimal
from utils.constants import headers_mutating_methods
from utils.dynamodb import initialize_dynamodb_tables
from utils.managers import join_product_stock
from utils.errors import BadRequestError


def lambda_handler(event, context):
    """Create product Lambda function handler."""

    try:
        # 0. Init

        products_table, stocks_table = initialize_dynamodb_tables()

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
        
        if not isinstance(price, (int, float, Decimal)):
            raise BadRequestError("Invalid request body: price should be a number")
        
        if not isinstance(count, int):
            raise BadRequestError("Invalid request body: count should be an integer")

        # 2. Create product and stock

        product = {
            "id": product_id,
            "title": title,
            "description": description,
            "price": str(price),
        }

        stock = {
            "product_id": product_id,
            "count": str(count),
        }

        # 3. Put product and stock into tables

        products_table.put_item(Item=product)
        stocks_table.put_item(Item=stock)

        joined_product_data = join_product_stock(product, [stock]) 

        # 4. Response
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
