import csv
import os
from dataclasses import dataclass
from typing import Dict, List

from src.models.stock_quote import StockQuote
from src.models.user import User


@dataclass
class CsvGenerator:

    file_name: str = "data.csv"
    working_dir: str = os.getenv("LOGS_WORKING_DIR", "./")

    def generate_csv(
        self, users: List[User], stock_quotes: Dict[str, StockQuote]
    ) -> None:
        data = []
        # TODO: Add in more data/columns EPS, PE, etc.
        for user in users:
            for strike_price in user.strike_prices:
                data.append(
                    [
                        user.email,
                        strike_price.symbol,
                        strike_price.buy_price,
                        strike_price.sell_price,
                        stock_quotes[strike_price.symbol].market_price,
                        stock_quotes[strike_price.symbol].trailing_pe,
                        stock_quotes[strike_price.symbol].forward_pe,
                        stock_quotes[strike_price.symbol].eps_current_year,
                        stock_quotes[strike_price.symbol].eps_forward,
                        stock_quotes[strike_price.symbol].eps_trailing_twelve_months,
                    ]
                )
        self._write_csv(
            column_headers=[
                "Email",
                "Stock",
                "Buy Price",
                "Sell Price",
                "Market Price",
                "Trailing PE",
                "Forward PE",
                "EPS Current Year",
                "EPS Forward",
                "EPS Trailing 12 Months",
            ],
            data=data,
        )

    def _write_csv(self, column_headers: list, data: List[list]) -> None:
        csv_data_with_headers = [column_headers] + data
        with open(self.working_dir + self.file_name, "w", newline="") as f:
            csv_writer = csv.writer(f)
            csv_writer.writerows(csv_data_with_headers)
