#!/usr/bin/env python3
import os

import aws_cdk as cdk

from authorization_service.authorization_service_stack import AuthorizationServiceStack

# 0. set environment variables

env = {
    "account": "730335652080",
    "region": "eu-north-1",
}

# 1. initialize the cdk app

app = cdk.App()

# .. Generate AWS CloudFormation template

app.synth()
