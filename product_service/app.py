#!/usr/bin/env python3
import os

import aws_cdk as cdk
from product_service.dynamo_db_stack import DynamoDBStack
from product_service.dynamo_db_stack import DynamoDBStack
from product_service.get_products_list_stack import GetProductsListStack
from product_service.get_product_by_id_stack import GetProductByIdStack
from product_service.create_product_stack import CreateProductStack
from product_service.lambda_catalog_batch_process_stack import LambdaCatalogBatchProcessStack
from product_service.api_gateway_stack import APIGatewayProductStack
from product_service.sqs_stack import SQSStack

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

# 3. create SQS stack

sqs_stack = SQSStack(
    app,
    id="SQS-Stack",
    env=cdk.Environment(**env),
)

# 4. create Lambda stacks

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

catalog_batch_process_stack = LambdaCatalogBatchProcessStack(
    app,
    construct_id="CatalogBatchProcessStack",
    dynamodb_stack=dynamodb_stack,
    sqs_stack=sqs_stack,
    env=cdk.Environment(**env),
)

# 5. create API Gateway stack as a trigger for Lambdas

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

APIGatewayProductStack(
    app,
    construct_id="APIGatewayProductStack",
    method_url_lambdas=urls,
    env=cdk.Environment(**env),
)

# 6. Generate AWS CloudFormation template

app.synth()
