from dataclasses import dataclass
from typing import Literal


@dataclass
class StockQuote:

    symbol: str
    name: str
    currency: Literal["USD"]
    market_price: float
