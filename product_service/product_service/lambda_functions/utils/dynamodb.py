import os
import boto3
from botocore.exceptions import ClientError


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


def execute_transact_write(items: list):
    """Execute transact write operation using low-level API."""
    dynamodb = boto3.client("dynamodb")
    try:
        dynamodb.transact_write_items(TransactItems=items)
    except ClientError as err:
        raise RuntimeError(f"Failed to execute DynamoDB transact write operation: {str(err)}") from err
