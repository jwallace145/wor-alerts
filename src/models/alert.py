from dataclasses import dataclass
from src.models.stock_quote import StockQuote

from src.models.strike_price import StrikePrice
from tabulate import tabulate
from typing import List
from src.utils.logger import Logger

log = Logger(__name__).get_logger()


@dataclass
class Alert:

    user_email: str
    strike_prices: List[StrikePrice]
    stock_quotes: List[StockQuote]

    def generate_alert_message(self) -> str:
        log.info(
            f"Sending alert message for {len(self.strike_prices)} stocks to user with email {self.user_email}....."
        )
        table = tabulate(
            tabular_data=self._generate_tabular_data(
                self.strike_prices, self.stock_quotes
            ),
            headers=[
                "Stock",
                "Buy",
                "Sell",
                "Market Price",
                "Trailing PE",
                "Forward PE",
                "EPS Current Year",
                "EPS Forward",
                "EPS Trailing 12 Months",
            ],
            tablefmt="floatfmt",
            numalign="right",
        )
        msg = (
            f"Hello, {self.user_email}!\n\n"
            f"Wolf of Robinhood has detected that {len(self.strike_prices)} of your stocks have breached the buy/sell criteria you specified."
            f" Below is a table of the stocks and their associated metrics. Please buy and sell accordingly.\n\n"
            f"{table}\n\n"
            f"Thanks and have a great day!\n"
            f"The Wolf of Robinhood Team"
        )
        return msg

    def _generate_tabular_data(
        self, strike_prices: List[StrikePrice], stock_quotes: List[StockQuote]
    ) -> List[list]:
        tabular_data = []
        for strike_price, stock_quote in zip(strike_prices, stock_quotes):
            tabular_data.append(
                [
                    strike_price.symbol,
                    strike_price.buy_price,
                    strike_price.sell_price,
                    stock_quote.market_price,
                    stock_quote.trailing_pe,
                    stock_quote.forward_pe,
                    stock_quote.eps_current_year,
                    stock_quote.eps_forward,
                    stock_quote.eps_trailing_twelve_months,
                ]
            )
        return tabular_data
