import os
import boto3

def initialize_dynamodb_tables():
    product_table_name = os.environ.get("PRODUCTS_TABLE_NAME")
    if not product_table_name:
        raise ValueError("Environment variable 'PRODUCTS_TABLE_NAME' not set")

    stocks_table_name = os.environ.get("STOCKS_TABLE_NAME")
    if not stocks_table_name:
        raise ValueError("Environment variable 'STOCKS_TABLE_NAME' not set")

    dynamodb = boto3.resource("dynamodb")
    products_table = dynamodb.Table(product_table_name)
    stocks_table = dynamodb.Table(stocks_table_name)

    return products_table, stocks_table