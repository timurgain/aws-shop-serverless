#!/usr/bin/env python3
import os

import aws_cdk as cdk

from import_service.s3_bucket_stack import S3BucketStack

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

# 3. Generate AWS CloudFormation template

app.synth()
