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
