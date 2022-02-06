import os
from dataclasses import dataclass
from typing import List

from mypy_boto3_dynamodb import DynamoDBClient
from src.aws_gateways.clients import dynamodb
from src.models.strike_price import StrikePrice
from src.models.user import User
from src.utils.logger import Logger

log = Logger(__name__).get_logger()


@dataclass
class DynamoDbGateway:

    client: DynamoDBClient = dynamodb
    strike_prices_table: str = os.getenv("STRIKE_PRICES_TABLE_NAME")

    def get_users(self) -> List[User]:
        log.info(self.strike_prices_table)
        items = self.client.scan(TableName=self.strike_prices_table)["Items"]
        users = []
        for item in items:
            user = User(
                email=item["email"]["S"], phone_number=item["phone_number"]["S"]
            )
            log.info(
                f"Creating user with email {user.email} and phone number {user.phone_number}....."
            )
            for item in item["strike_prices"]["L"]:
                strike_price = StrikePrice(
                    symbol=item["M"]["symbol"]["S"],
                    buy_price=float(item["M"]["buy_price"]["N"]),
                    sell_price=float(item["M"]["sell_price"]["N"]),
                )
                user.strike_prices.append(strike_price)
                log.info(
                    f"Adding stock {strike_price.symbol} with buy price {strike_price.buy_price} and sell price {strike_price.sell_price} to user with email {user.email}....."
                )
            users.append(user)
        return users
