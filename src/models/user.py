from dataclasses import dataclass, field
from typing import List, Optional
from src.models.strike_price import StrikePrice


@dataclass
class User:

    email: str
    phone_number: str
    strike_prices: Optional[List[StrikePrice]] = field(default_factory=lambda: [])
