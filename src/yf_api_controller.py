import json
from dataclasses import asdict, dataclass

import requests

from src.models.stock_quote import StockQuote
from src.utils.logger import Logger

BASE_URL = "https://yfapi.net"
GET_STOCK_QUOTE = "/v6/finance/quote"

log = Logger(__name__).get_logger()


@dataclass
class YFApiController:

    api_key: str

    def get_stock_quote(self, symbol: str) -> StockQuote:
        log.info(f"Getting stock quote for symbol {symbol}.....")
        response = requests.request(
            "GET",
            f"{BASE_URL}{GET_STOCK_QUOTE}",
            headers={"x-api-key": self.api_key},
            params={"symbols": symbol},
        ).json()["quoteResponse"]["result"][0]
        stock_quote = StockQuote(
            symbol=symbol,
            name=response["displayName"],
            currency=response["currency"],
            market_price=response["regularMarketPrice"],
        )
        log.info(
            f"Stock quote for symbol {symbol}:\n{json.dumps(asdict(stock_quote), indent=4)}"
        )
        return stock_quote
