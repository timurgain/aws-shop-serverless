from decimal import Decimal
import os
import boto3
from botocore.exceptions import ClientError

from utils.errors import BadRequestError
# from product_service.product_service.lambda_functions.utils.errors import BadRequestError



def get_products_table_name():
    """Get product table name from environment variables."""
    product_table_name = os.environ.get("PRODUCTS_TABLE_NAME", None)
    if not product_table_name:
        raise ValueError("Environment variable 'PRODUCTS_TABLE_NAME' not set")
    return product_table_name


def get_stocks_table_name():
    """Get stock table name from environment variables."""
    stocks_table_name = os.environ.get("STOCKS_TABLE_NAME", None)
    if not stocks_table_name:
        raise ValueError("Environment variable 'STOCKS_TABLE_NAME' not set")
    return stocks_table_name


def initialize_dynamodb_tables():
    """Initialize DynamoDB tables for high-level API usage."""
    product_table_name = get_products_table_name()
    stocks_table_name = get_stocks_table_name()

    dynamodb = boto3.resource("dynamodb")
    products_table = dynamodb.Table(product_table_name)
    stocks_table = dynamodb.Table(stocks_table_name)

    return products_table, stocks_table


def prepare_product_stock_data(
    product_id: str, title: str, description: str, price: Decimal, count: int = 0
):
    """Prepare product and stock data for DynamoDB TransactWriteItems operation."""

    # 0. Validate input data

    if not title or not description or not price:
        raise BadRequestError(
            "Invalid request body: title, description and price are required"
        )

    if not isinstance(price, (int, float, Decimal)) or not price > 0:
        raise BadRequestError("Invalid request body: price should be a positive number")

    if not isinstance(count, int) or not count >= 0:
        raise BadRequestError(
            "Invalid request body: count should be an integer that is greater or equal to 0"
        )

    # 1. Prepare product data and stock data for DynamoDB TransactWriteItems operation

    product = {
        "Put": {
            "TableName": get_products_table_name(),
            "Item": {
                "id": {"S": product_id},
                "title": {"S": title},
                "description": {"S": description},
                "price": {"N": str(price)},
            },
        }
    }

    stock = {
        "Put": {
            "TableName": get_stocks_table_name(),
            "Item": {
                "product_id": {"S": product_id},
                "count": {"N": str(count)},
            },
        }
    }

    return [product, stock]


def execute_transact_write(items: list):
    """Execute transact write operation using low-level API."""
    dynamodb = boto3.client("dynamodb")
    try:
        dynamodb.transact_write_items(TransactItems=items)
    except ClientError as err:
        raise RuntimeError(
            f"Failed to execute DynamoDB transact write operation: {str(err)}"
        ) from err
