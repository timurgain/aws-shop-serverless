#!/usr/bin/env python3
import os

import aws_cdk as cdk

from aws_shop_serverless.get_products_list_stack import GetProductsListStack
from aws_shop_serverless.get_product_by_id_stack import GetProductByIdStack

from aws_shop_serverless.api_gateway import APIGatewayStack

# 0. set environment variables

env = {
    "account": "730335652080",
    "region": "eu-north-1",
}


# 1. initialize the cdk app

app = cdk.App()

# 2. create Lambda stacks

get_products_list_stack = GetProductsListStack(
    app,
    construct_id="GetProductsListStack",
    env=cdk.Environment(**env),
)

get_product_by_id_stack = GetProductByIdStack(
    app,
    construct_id="GetProductByIdStack",
    env=cdk.Environment(**env),
)

# 3. create API Gateway stack as a trigger for Lambdas

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
]

APIGatewayStack(
    app,
    construct_id="APIGatewayStack",
    env=cdk.Environment(**env),
    method_url_lambdas=urls,
)

# 4. Generate AWS CloudFormation template

app.synth()
