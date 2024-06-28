#!/usr/bin/env python3
import os

import aws_cdk as cdk

from import_service.s3_bucket_stack import S3BucketStack
from import_service.import_products_file_stack import ImportProductsFileStack

from import_service.api_gateway_stack import APIGatewayStack


# 0. set environment variables

env = {
    "account": "730335652080",
    "region": "eu-north-1",
}

# 1. initialize the cdk app

app = cdk.App()

# 2. create S3 Bucket stack

s3_bucket_stack = S3BucketStack(
    app,
    construct_id="TM-Shop-Import-Service-S3-Bucket",
    env=cdk.Environment(**env),
)

# 3. create Lambda stacks

import_products_file_stack = ImportProductsFileStack(
    app,
    construct_id="ImportProductsFileStack",
    s3_bucket_stack=s3_bucket_stack,
    env=cdk.Environment(**env),
)

# 4. create API Gateway stack as a trigger for Lambdas

urls = [
    (
        "POST",
        "import",
        import_products_file_stack.import_products_file,
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
