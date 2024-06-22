import json
import http
from utils.serializers import DecimalEncoder
from utils.constants import headers_safe_methods
from utils.managers import join_product_stock
from utils.dynamodb import initialize_dynamodb_tables
from utils.errors import NotFoundError


def lambda_handler(event, context):
    """Get product by ID Lambda function handler."""

    try:

        # 0. Init

        products_table, stocks_table = initialize_dynamodb_tables()

        # 1. Get product by ID

        product_id = event.get("pathParameters", {}).get("product_id")
        product = products_table.get_item(Key={"id": product_id}).get("Item")
        stocks = stocks_table.scan().get("Items", [])
        if product is None:
            raise NotFoundError("Product not found")
        
        joined_product_data = join_product_stock(product, stocks)

        # 2. Response

        return {
            "headers": headers_safe_methods,
            "statusCode": http.HTTPStatus.OK,
            "body": json.dumps(joined_product_data, cls=DecimalEncoder),
        }
        
    except NotFoundError as err:
        return {
            "headers": headers_safe_methods,
            "statusCode": http.HTTPStatus.NOT_FOUND,
            "body": json.dumps({"error": str(err)}),
        }
    
    except Exception as err:
        return {
            "headers": headers_safe_methods,
            "statusCode": http.HTTPStatus.INTERNAL_SERVER_ERROR,
            "body": json.dumps(str(err)),
        }
