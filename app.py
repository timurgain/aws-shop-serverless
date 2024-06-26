#!/usr/bin/env python3
import os

import aws_cdk as cdk

from aws_shop_serverless.dynamo_db_stack import DynamoDBStack
from aws_shop_serverless.get_products_list_stack import GetProductsListStack
from aws_shop_serverless.get_product_by_id_stack import GetProductByIdStack
from aws_shop_serverless.create_product_stack import CreateProductStack

from aws_shop_serverless.api_gateway_stack import APIGatewayStack

# 0. set environment variables

env = {
    "account": "730335652080",
    "region": "eu-north-1",
}


# 1. initialize the cdk app

app = cdk.App()

# 2. create DynamoDB stack

dynamodb_stack = DynamoDBStack(
    app,
    construct_id="Shop-DynamoDB-",
    env=cdk.Environment(**env)
) 

# 3. create Lambda stacks

get_products_list_stack = GetProductsListStack(
    app,
    construct_id="GetProductsListStack",
    dynamodb_stack=dynamodb_stack,
    env=cdk.Environment(**env),
)

get_product_by_id_stack = GetProductByIdStack(
    app,
    construct_id="GetProductByIdStack",
    dynamodb_stack=dynamodb_stack,
    env=cdk.Environment(**env),
)

create_product_stack = CreateProductStack(
    app,
    construct_id="CreateProductStack",
    dynamodb_stack=dynamodb_stack,
    env=cdk.Environment(**env),
)

# 4. create API Gateway stack as a trigger for Lambdas

urls = [
    (
        "GET",
        "products",
        get_products_list_stack.get_products,
    ),
    (
        "GET",
        "products/{product_id}",
        get_product_by_id_stack.get_product_by_id,
    ),
    (
        "POST",
        "products",
        create_product_stack.create_product,
    ),
]

APIGatewayStack(
    app,
    construct_id="APIGatewayStack",
    env=cdk.Environment(**env),
    method_url_lambdas=urls,
)

# 5. Generate AWS CloudFormation template

app.synth()
