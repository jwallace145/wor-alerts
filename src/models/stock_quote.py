from dataclasses import dataclass
from typing import Literal


@dataclass
class StockQuote:

    symbol: str
    name: str
    currency: Literal["USD"]
    market_price: float
    trailing_pe: float
    forward_pe: float
    eps_current_year: float
    eps_forward: float
    eps_trailing_twelve_months: float
