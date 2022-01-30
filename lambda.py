import json
import os
from dataclasses import asdict

from src.yf_api_controller import YFApiController


def lambda_handler(event, context):
    yf_api = YFApiController(os.getenv("YF_API_KEY"))
    msft_stock_quote = yf_api.get_stock_quote("MSFT")
    return {"statusCode": 200, "body": json.dumps(asdict(msft_stock_quote), indent=4)}
