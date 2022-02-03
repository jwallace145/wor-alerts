from dataclasses import dataclass
from typing import Optional


@dataclass
class StrikePrice:

    symbol: str
    buy_price: Optional[float]
    sell_price: Optional[float]
