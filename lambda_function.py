import json

import os
from src.actualizer import Actualizer


def lambda_handler(event, context):
    # create actualizer
    actualizer = Actualizer(logs_working_dir=os.getenv("LOGS_WORKING_DIR"))

    # get users from database
    users = actualizer.get_users()

    # get all the stock data that the users want to track
    stock_quotes = actualizer.get_stock_quotes(users)

    # publish alert messages if user provided thresholds are breached
    actualizer.publish_alert_messages(users, stock_quotes)

    # write invocation digest to s3 bucket
    actualizer.write_digest_to_s3_bucket(users, stock_quotes)

    # TODO: Write logs to file and upload to s3 bucket

    return {"statusCode": 200, "body": json.dumps("wolf or robinhood!")}
