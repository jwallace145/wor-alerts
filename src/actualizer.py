from dataclasses import dataclass
from typing import Dict, List, Set

from src.gateways.dynamodb_gateway import DynamoDbGateway
from src.gateways.s3_gateway import S3Gateway
from src.gateways.sns_gateway import SnsGateway
from src.models.stock_quote import StockQuote
from src.models.user import User
from src.utils.csv_generator import CsvGenerator
from src.utils.logger import Logger
from src.yf_api_controller import YFApiController

log = Logger(__name__).get_logger()


@dataclass
class Actualizer:

    yf_api: YFApiController = YFApiController()
    dynamodb_gateway: DynamoDbGateway = DynamoDbGateway()
    s3_gateway: S3Gateway = S3Gateway()
    sns_gateway: SnsGateway = SnsGateway()
    csv_generator: CsvGenerator = CsvGenerator()

    def get_users(self) -> List[User]:
        return self.dynamodb_gateway.get_users()

    def get_stock_quotes(self, users: List[User]) -> Dict[str, StockQuote]:
        return self.yf_api.get_stock_quotes(symbols=self._get_symbols(users))

    def publish_alert_messages(
        self, users: List[User], stock_quotes: Dict[str, StockQuote]
    ) -> None:
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
                        f" During the last Wolf of Robinhood query, stock {strike_price.symbol} had a market price of ${market_price}.\n\n"
                        f"Thanks and have a great day!\n"
                        f"The Wolf of Robinhood Team"
                    )
                    self.sns_gateway.publish_message(message=msg)
                elif strike_price.sell_price < market_price:
                    log.info(
                        f"Sending sell alert message for stock {strike_price.symbol} to email {user.email} and phone number {user.phone_number}"
                    )
                    msg = (
                        f"Hello, {user.email}!\n\n"
                        f"Wolf of Robinhood has detected that your stock {strike_price.symbol} has breached the sell price you set of ${strike_price.sell_price}."
                        f" During the last Wolf of Robinhood query, stock {strike_price.symbol} had a market price of ${market_price}.\n\n"
                        f"Thanks and have a great day!\n"
                        f"The Wolf of Robinhood Team"
                    )
                    self.sns_gateway.publish_message(message=msg)

    def write_digest_to_s3_bucket(
        self, users: List[User], stock_quotes: Dict[str, StockQuote]
    ) -> None:
        self.csv_generator.generate_csv(users, stock_quotes)
        self.s3_gateway.upload_file(file_name="/tmp/data.csv", key="data.csv")
        self.s3_gateway.upload_file(file_name="/tmp/logs.log", key="logs.log")

    @staticmethod
    def _get_symbols(users: List[User]) -> Set[str]:
        symbols = set()
        for user in users:
            for strike_price in user.strike_prices:
                if strike_price.symbol not in symbols:
                    symbols.add(strike_price.symbol)
        return symbols
