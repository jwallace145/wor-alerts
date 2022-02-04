import csv
from dataclasses import dataclass
from typing import Dict, List

from src.models.stock_quote import StockQuote
from src.models.user import User


@dataclass
class CsvGenerator:

    file_name: str = "data.csv"
    working_dir: str = "/tmp/"

    def generate_csv(
        self, users: List[User], stock_quotes: Dict[str, StockQuote]
    ) -> None:
        data = []
        for user in users:
            for strike_price in user.strike_prices:
                data.append(
                    [
                        user.email,
                        strike_price.symbol,
                        strike_price.buy_price,
                        strike_price.sell_price,
                        stock_quotes[strike_price.symbol].market_price,
                    ]
                )
        self._write_csv(
            column_headers=[
                "email",
                "stock",
                "buy price",
                "sell price",
                "market price",
            ],
            data=data,
        )

    def _write_csv(self, column_headers: list, data: List[list]) -> None:
        csv_data_with_headers = [column_headers] + data
        with open(self.working_dir + self.file_name, "w", newline="") as f:
            csv_writer = csv.writer(f)
            csv_writer.writerows(csv_data_with_headers)
