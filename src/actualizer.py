from dataclasses import dataclass
from typing import Dict, List, Set
from datetime import datetime

from src.aws_gateways.dynamodb_gateway import DynamoDbGateway
from src.aws_gateways.s3_gateway import S3Gateway
from src.aws_gateways.sns_gateway import SnsGateway
from src.models.stock_quote import StockQuote
from src.models.user import User
from src.utils.csv_generator import CsvGenerator
from src.utils.logger import Logger
from src.yahoo_finance.yf_api_controller import YFApiController
from src.aws_gateways.ses_gateway import SesGateway

log = Logger(__name__).get_logger()


@dataclass
class Actualizer:

    logs_working_dir: str = "./"
    yf_api: YFApiController = YFApiController()
    dynamodb_gateway: DynamoDbGateway = DynamoDbGateway()
    s3_gateway: S3Gateway = S3Gateway()
    ses_gateway: SesGateway = SesGateway()
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
            alert_strike_prices = []
            alert_stock_quotes = []
            for strike_price in user.strike_prices:
                market_price = stock_quotes[strike_price.symbol].market_price
                if (
                    strike_price.buy_price > market_price
                    or strike_price.sell_price < market_price
                ):
                    alert_strike_prices.append(strike_price)
                    alert_stock_quotes.append(stock_quotes[strike_price.symbol])
            if len(alert_strike_prices) > 0:
                # self.sns_gateway.publish_message(
                #     message=Alert(
                #         user_email=user.email,
                #         strike_prices=alert_strike_prices,
                #         stock_quotes=alert_stock_quotes,
                #     ).generate_alert_message()
                # )
                log.info(f"sending alert message to {user.email}")
                self.ses_gateway.send_email(
                    user=user,
                    strike_prices=alert_strike_prices,
                    stock_quotes=alert_stock_quotes,
                )

    def write_digest_to_s3_bucket(
        self, users: List[User], stock_quotes: Dict[str, StockQuote]
    ) -> None:
        self.csv_generator.generate_csv(users, stock_quotes)
        key_prefix = self._get_key_prefix_timestamp()
        self.s3_gateway.upload_file(
            file_name=f"{self.logs_working_dir}data.csv",
            key=f"{key_prefix}data.csv",
        )
        self.s3_gateway.upload_file(
            file_name=f"{self.logs_working_dir}logs.log", key=f"{key_prefix}logs.log"
        )

    @staticmethod
    def _get_symbols(users: List[User]) -> Set[str]:
        symbols = set()
        for user in users:
            for strike_price in user.strike_prices:
                if strike_price.symbol not in symbols:
                    symbols.add(strike_price.symbol)
        return symbols

    @staticmethod
    def _get_key_prefix_timestamp() -> str:
        timestamp = datetime.today()
        return f"{timestamp.year}/{timestamp.month}/{timestamp.day}/{timestamp.hour}{timestamp.minute}"
