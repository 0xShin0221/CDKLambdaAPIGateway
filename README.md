
PythonでCDKを使ってLambda・APIGatewayスタックの作成Tip

記事は[こちら](https://code-recipies.netlify.com/tips/IaaS/cdk/lambda-apigateway)

---
title: PythonでCDKを使ってLambda・APIGatewayスタックの作成Tip
description: PythonでLamda・API Gatewayをcdkで構築
---

## Introduction
PythonでAWS CDKでLambda,APIGatewayのスタックを作成

## TL;DR
- CDKでLambda・APIGatewayのスタックを作成しデプロイ・検証
- Python

## 前提
事前にcdkをインストール済み

```sh title=cdkのインストール
$ npm install -g aws-cdk
```

## CDKでPython環境を構築しLambdaとAPIGatewayをインストール

空フォルダで作成する必要があるので作成しCDK cliでpython環境を構築

```sh title=cdk cliでpython環境の構築
$ mkdir LambdaAPIGatewaySample
$ cd LambdaAPIGatewaySample
$ cdk init --language=python
```

今回LambdaとAPIGatewayをcdkからインストールするので,`setup.py`に追記

```python title=setup.py
...
    install_requires=[
        "aws-cdk.core==1.32.1",
        "aws-cdk.aws-lambda", #追加
        "aws-cdk.aws-apigateway", #追記
    ],
...
```

CDK initで作成された仮想環境で下記を実行

```sh 
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

## Lambda関数作成

```sh
$ mkdir lambda
$ touch lambda/api.py
```

作成した`api.py`を実装

```python title=api.py
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def main(event, context):
    logger.info(json.dumps(event))

    return {
        'statusCode': 200,
        'body': 'Hello World'
    }
```

### Stackを追加

CDKでスタックを指定している`/lambda_api_gateway_sample/lambda_api_gateway_sample_stack.py`を下記に編集

```python title=lambda_api_gateway_sample_stack.py
from aws_cdk import (
    aws_lambda,
    aws_apigateway,
    core
)

class LambdaApiGatewaySampleStack(core.Stack): #このClass名は各自の環境で変わるので注意

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        handler = aws_lambda.Function(
            self, "cdk-lambda-apigateway",
            runtime=aws_lambda.Runtime.PYTHON_3_7,
            handler="api.main",
            code=aws_lambda.AssetCode(path="./lambda"))

        api = aws_apigateway.LambdaRestApi(self, "LambdawithAPIGateway", handler=handler) #第二引数のAPIGatewayの命名は
```


保存したらDeployしてみましょう.`cdk deploy`成功するとこんな感じ

```title=deploy成功

✅  lambda-api-gateway-sample

Outputs:
lambda-api-gateway-sample.LambdawithAPIGatewayEndpointXXXXXXX = https://xxxxxxx.execute-api.us-east-1.amazonaws.com/prod/

Stack ARN:
arn:aws:cloudformation:us-east-1:xxxxxxxxxxxx:stack/lambda-api-gateway-sample/xxxxxxxxxxxxxxxxxx
```

## 検証

curlでdeploy後のEndpointにリクエストをし`Hello world`で検証完了です。

```sh 
$ curl https://xxxxxxxx.execute-api.us-east-1.amazonaws.com/prod
Hello World
```

気になるのが、CFnで書いた時の比較ですが、テンプレートファイルは下記で作成できます。400行近くのymlファイルが20行程のPythonファイルで生成されるので便利ですね。

```sh
$ cdk synth --no-staging > template.yml
```

また、生成されたCFnのテンプレートファイルとSAM CLIを用いてとローカル環境で検証するができます

```sh
$ sam local start-api -t template.yaml
```

検証したら忘れないうちに
`$ cdk destroy`
