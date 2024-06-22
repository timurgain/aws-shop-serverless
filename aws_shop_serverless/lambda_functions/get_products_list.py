import os
import json
import boto3
from utils.serializers import DecimalEncoder
from utils.constants import headers_safe_methods
from utils.managers import join_product_stock


def lambda_handler(event, context):
    try:
        # 0. Init

        product_table_name = os.environ.get("PRODUCTS_TABLE_NAME")
        stocks_table_name = os.environ.get("STOCKS_TABLE_NAME")

        dynamodb = boto3.resource("dynamodb")
        products_table = dynamodb.Table(product_table_name)
        stocks_table = dynamodb.Table(stocks_table_name)

        # 1. Get all products and stocks

        products = products_table.scan().get("Items", [])
        stocks = stocks_table.scan().get("Items", [])
        joined_products_data = [
            join_product_stock(product, stocks) for product in products
        ]

        # 2. response

        return {
            "headers": headers_safe_methods,
            "statusCode": 200,
            "body": json.dumps(joined_products_data, cls=DecimalEncoder),
        }

    except Exception as err:
        return {
            "headers": headers_safe_methods,
            "statusCode": 500,
            "body": json.dumps(str(err)),
        }
