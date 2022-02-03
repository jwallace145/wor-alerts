from dataclasses import dataclass
from src.models.user import User
from src.yf_api_controller import YFApiController
from src.gateways.dynamodb_gateway import DynamoDbGateway
from src.gateways.sns_gateway import SnsGateway
from typing import List, Set
from src.utils.logger import Logger

log = Logger(__name__).get_logger()


@dataclass
class Actualizer:

    yf_api: YFApiController = YFApiController()
    dynamodb_gateway: DynamoDbGateway = DynamoDbGateway()
    sns_gateway: SnsGateway = SnsGateway()

    def get_stocks_and_publish_messages(self):
        # get user strike prices
        users = self.dynamodb_gateway.get_users()

        # get set of stocks to query
        symbols = self._get_symbols(users)

        # query yf api for user strike prices
        stock_quotes = self.yf_api.get_stock_quotes(symbols=symbols)

        # do comparison and publish sns message if criteria is met
        for user in users:
            for strike_price in user.strike_prices:
                market_price = stock_quotes[strike_price.symbol].market_price
                if strike_price.buy_price > market_price:
                    log.info(
                        f"Sending buy alert message for stock {strike_price.symbol} to email {user.email} and phone number {user.phone_number}"
                    )
                    msg = (
                        f"Hello, {user.email}!\n\n"
                        f"Wolf of Robinhood has detected that your stock {strike_price.symbol} has breached the buy price you set of ${strike_price.buy_price}."
                        f" During the last Wolf of Robinhood query, stock {strike_price.symbol} had a market price of {market_price}.\n\n"
                        f"Thanks and have a great day!\n"
                        f"The Wolf of Robinhood Team"
                    )
                    self.sns_gateway.publish_message(message=msg)
                if strike_price.sell_price < market_price:
                    log.info(
                        f"Sending sell alert message for stock {strike_price.symbol} to email {user.email} and phone number {user.phone_number}"
                    )
                    msg = (
                        f"Hello, {user.email}!\n\n"
                        f"Wolf of Robinhood has detected that your stock {strike_price.symbol} has breached the sell price you set of ${strike_price.sell_price}."
                        f" During the last Wolf of Robinhood query, stock {strike_price.symbol} had a market price of {market_price}.\n\n"
                        f"Thanks and have a great day!\n"
                        f"The Wolf of Robinhood Team"
                    )
                    self.sns_gateway.publish_message(message=msg)

    @staticmethod
    def _get_symbols(users: List[User]) -> Set[str]:
        symbols = set()
        for user in users:
            for strike_price in user.strike_prices:
                if strike_price.symbol not in symbols:
                    symbols.add(strike_price.symbol)
        return symbols
