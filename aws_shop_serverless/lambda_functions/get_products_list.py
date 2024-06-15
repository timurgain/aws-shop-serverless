import json

# from aws_shop_serverless.mock.production_list import production_list


def lambda_handler(event, context):
    mock_production_list = [
        {"id": 1, "title": "Product 1", "color": "red", "price": 100},
        {"id": 2, "title": "Product 2", "color": "blue", "price": 200},
        {"id": 3, "title": "Product 3", "color": "green", "price": 300},
    ]

    return {
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
        },
        "statusCode": 200,
        "body": json.dumps(mock_production_list),
    }
