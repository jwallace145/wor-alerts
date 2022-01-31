from dataclasses import dataclass
from typing import Dict

import requests

from src.models.stock_quote import StockQuote
from src.utils.logger import Logger

BASE_URL = "https://yfapi.net"
GET_STOCK_QUOTE = "/v6/finance/quote"

log = Logger(__name__).get_logger()


@dataclass
class YFApiController:

    api_key: str

    def get_stock_quotes(self, symbols: str) -> Dict[str, StockQuote]:
        log.info(f"Getting stock quotes for symbols {symbols.split(sep=',')}.....")
        response = requests.request(
            "GET",
            f"{BASE_URL}{GET_STOCK_QUOTE}",
            headers={"x-api-key": self.api_key},
            params={"symbols": symbols},
        ).json()["quoteResponse"]["result"]
        stock_quotes = {}
        for quote in response:
            stock_quotes[quote["symbol"]] = StockQuote(
                symbol=quote["symbol"],
                name=quote["displayName"],
                currency=quote["currency"],
                market_price=quote["regularMarketPrice"],
            )
        return stock_quotes
