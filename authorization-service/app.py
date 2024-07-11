#!/usr/bin/env python3
import os

import aws_cdk as cdk
from dotenv import load_dotenv

from authorization_service.basic_authorizer_stack import BasicAuthorizerStack

# 0. set environment variables

load_dotenv()

env_cdk = {
    "account": "730335652080",
    "region": "eu-north-1",
}

env_app = {
    "GITHUB_ACCOUNT_LOGIN": os.getenv('GITHUB_ACCOUNT_LOGIN'),
    "TEST_PASSWORD": os.getenv('TEST_PASSWORD'),
}

# 1. initialize the cdk app

app = cdk.App()

# 2. create Basic Authorizer stack

BasicAuthorizerStack(
    app,
    construct_id="BasicAuthorizer",
    env_app=env_app,
    env=cdk.Environment(**env_cdk),
)

# .. Generate AWS CloudFormation template

app.synth()
