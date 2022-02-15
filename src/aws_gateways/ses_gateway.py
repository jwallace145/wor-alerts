import os
from dataclasses import dataclass
from typing import List

from mypy_boto3_ses import SESClient
from src.aws_gateways.clients import ses
from src.models.stock_quote import StockQuote
from src.models.strike_price import StrikePrice
from src.models.user import User

SES_SOURCE_EMAIL = os.getenv("SES_SOURCE_EMAIL")
SES_TEMPLATE = os.getenv("SES_TEMPLATE")


@dataclass
class SesGateway:

    ses_client: SESClient = ses

    # CRUD methods for templates
    def get_template(self) -> None:
        self.ses_client.get_template(TemplateName=SES_TEMPLATE)

    def create_template(self) -> None:
        self.ses_client.create_template(
            Template={
                "TemplateName": SES_TEMPLATE,
                "SubjectPart": "",
                "TextPart": "",
                "HtmlPart": "",
            }
        )

    def update_template(self, template_file_path: str, subject: str) -> None:
        self.ses_client.update_template(
            Template={
                "TemplateName": SES_TEMPLATE,
                "SubjectPart": subject,
                "TextPart": "This is the text part",
                "HtmlPart": open(template_file_path, "r").read(),
            }
        )

    def delete_template(self) -> None:
        self.ses_client.delete_template(TemplateName=SES_TEMPLATE)

    def _generate_template_data(
        self,
        user: User,
        strike_prices: List[StrikePrice],
        stock_quotes: List[StockQuote],
    ) -> str:
        user_str = '{ "user": { "email": "%s" },' % user.email
        strike_prices_str = ' "strike_prices": ['
        for i, strike_price in enumerate(strike_prices):
            strike_prices_str += (
                ' { "symbol": "%s", "buy_price": %f, "sell_price": %f }'
                % (strike_price.symbol, strike_price.buy_price, strike_price.sell_price)
            )
            if i != len(strike_prices) - 1:
                strike_prices_str += ","
        strike_prices_str += "]}"
        template_data = user_str + strike_prices_str
        return template_data

    def send_email(
        self,
        user: User,
        strike_prices: List[StrikePrice],
        stock_quotes: List[StockQuote],
    ) -> str:

        return self.ses_client.send_templated_email(
            Source=SES_SOURCE_EMAIL,
            Destination={"ToAddresses": [user.email]},
            Template=SES_TEMPLATE,
            TemplateData=self._generate_template_data(
                user=user, strike_prices=strike_prices, stock_quotes=stock_quotes
            ),
        )["MessageId"]
