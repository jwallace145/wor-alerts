import json
import os
from dataclasses import asdict, dataclass

import requests

from src.models.stock_quote import StockQuote
from src.utils.logger import Logger
from typing import Set, Dict

BASE_URL = "https://yfapi.net"
GET_STOCK_QUOTE = "/v6/finance/quote"

log = Logger(__name__).get_logger()


@dataclass
class YFApiController:

    api_key: str = os.getenv("YF_API_KEY")

    def get_stock_quotes(self, symbols: Set[str]) -> Dict[str, StockQuote]:
        log.info(f"Getting stock quotes for symbols {symbols}.....")
        response = requests.request(
            "GET",
            f"{BASE_URL}{GET_STOCK_QUOTE}",
            headers={"x-api-key": self.api_key},
            params={"symbols": self._parse_symbols_set(symbols)},
        ).json()["quoteResponse"]["result"]
        stock_quotes = {}
        for item in response:
            stock_quote = StockQuote(
                symbol=item["symbol"],
                name=item["displayName"],
                currency=item["currency"],
                market_price=item["regularMarketPrice"],
            )
            stock_quotes[item["symbol"]] = stock_quote
        log.info(
            f"Stock quotes from yahoo finance:\n{json.dumps({key: asdict(value) for key, value in stock_quotes.items()}, indent=4)}"
        )
        return stock_quotes

    @staticmethod
    def _parse_symbols_set(symbols: Set[str]) -> str:
        symbols_str = ""
        for symbol in symbols:
            symbols_str += symbol + ","
        return symbols_str[:-1]
