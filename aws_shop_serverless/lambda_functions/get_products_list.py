import json


def lambda_handler(event, context):

    # 0. constants

    mock_production_list = [
        {"id": 1, "title": "Product 1", "color": "red", "price": 100},
        {"id": 2, "title": "Product 2", "color": "blue", "price": 200},
        {"id": 3, "title": "Product 3", "color": "green", "price": 300},
    ]

    # 1. response

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
