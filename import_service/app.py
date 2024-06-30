#!/usr/bin/env python3
import os

import aws_cdk as cdk
from aws_cdk.aws_lambda_event_sources import S3EventSource

from import_service.import_products_file_stack import ImportShopProductsFileStack

from import_service.api_gateway_stack import APIGatewayImportFileStack


# 0. set environment variables

env = {
    "account": "730335652080",
    "region": "eu-north-1",
}

# 1. initialize the cdk app

app = cdk.App()

# 2. create S3 bucket and lambda stack

import_service_stack = ImportShopProductsFileStack(
    app,
    construct_id="ImportShopProductsFileStack",
    env=cdk.Environment(**env),
)

# 3. create API Gateway stack as a trigger for the import_products_file lambda

urls = [
    (
        ["GET", "OPTIONS", "PUT", "POST", "DELETE"],
        "import",
        import_service_stack.import_products_file,
    ),
]

APIGatewayImportFileStack(
    app,
    construct_id="APIGatewayImportFileStack",
    env=cdk.Environment(**env),
    method_url_lambdas=urls,
)

# 6. Generate AWS CloudFormation template

app.synth()
