#!/usr/bin/env python3

from aws_cdk import core

from lambda_api_gateway_sample.lambda_api_gateway_sample_stack import LambdaApiGatewaySampleStack


app = core.App()
LambdaApiGatewaySampleStack(app, "lambda-api-gateway-sample")

app.synth()
