from aws_cdk import (
    aws_lambda,
    aws_apigateway,
    core
)

class LambdaApiGatewaySampleStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        handler = aws_lambda.Function(
            self, "cdk-lambda-apigateway",
            runtime=aws_lambda.Runtime.PYTHON_3_7,
            handler="api.main",
            code=aws_lambda.AssetCode(path="./lambda"))

        api = aws_apigateway.LambdaRestApi(self, "LambdawithAPIGateway", handler=handler)