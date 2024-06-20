import json


def lambda_handler(event, context):

    # 0. Constants

    mock_production_list = [
        {"id": 1, "title": "Product 1", "color": "red", "price": 100},
        {"id": 2, "title": "Product 2", "color": "blue", "price": 200},
        {"id": 3, "title": "Product 3", "color": "green", "price": 300},
    ]

    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
    }

    # 1. Get product ID

    try:
        product_id = int(event["pathParameters"]["product_id"])
    except (KeyError, ValueError):
        return {
            "headers": headers,
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid product ID type"}),
        }

    # 2. Get product by ID

    product = next(
        (product for product in mock_production_list if product["id"] == product_id),
        None,
    )

    # 3. Response

    if product is None:
        return {
            "headers": headers,
            "statusCode": 404,
            "body": json.dumps({"error": "Product not found"}),
        }
    else:
        return {
            "headers": headers,
            "statusCode": 200,
            "body": json.dumps(product),
        }
