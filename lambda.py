import json
import os

from src.gateways.sns_gateway import SnsGateway
from src.utils.logger import Logger
from src.yf_api_controller import YFApiController

STOCKS = "MSFT,AAPL,PYPL"
STRIKE_PRICES = {"MSFT": 320.00, "AAPL": 165.00, "PYPL": 170.00}

log = Logger(__name__).get_logger()


def lambda_handler(event, context):
    yf_api = YFApiController(os.getenv("YF_API_KEY"))
    stock_quotes = yf_api.get_stock_quotes(symbols=STOCKS)

    sns_gateway = SnsGateway(topic_arn=os.getenv("SNS_TOPIC_ARN"))
    for stock, strike_price in STRIKE_PRICES.items():
        market_price = stock_quotes[stock].market_price
        if market_price > strike_price:
            log.info(
                f"Strike price for stock {stock} exceeded! Publishing message to SNS topic now....."
            )
            sns_gateway.publish_message(
                message=f"yo sell {stock} because its market price is ${market_price}"
                f" which is above the strike price of ${strike_price}"
            )
        else:
            log.info(f"Strike price for stock {stock} not exceeded. Hold for now.....")
    return {"statusCode": 200, "body": json.dumps("The Wolf of Robinhood")}
