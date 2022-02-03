import json

from src.actualizer import Actualizer


def lambda_handler(event, context):
    Actualizer().get_stocks_and_publish_messages()
    return {"statusCode": 200, "body": json.dumps("wolf or robinhood!")}
