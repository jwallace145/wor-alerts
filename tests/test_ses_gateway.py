import pytest
import json
from src.aws_gateways.ses_gateway import SesGateway


class TestSesGateway:
    @pytest.fixture(autouse=True)
    def init_test_ses_gateway(self, mock_ses):
        self.ses_gateway = SesGateway(ses_client=mock_ses)

    def test_generate_template_data(
        self, mock_user, mock_strike_price, mock_stock_quote
    ):
        template_data = self.ses_gateway._generate_template_data(
            user=mock_user,
            strike_prices=[mock_strike_price],
            stock_quotes=[mock_stock_quote],
        )
        assert json.loads(template_data) == {
            "user": {"email": "testuser@gmail.com"},
            "strike_prices": [
                {
                    "symbol": "MSFT",
                    "buy_price": 200.00,
                    "sell_price": 300.00,
                    "market_price": 310.00,
                    "trailing_pe": 1.00,
                    "forward_pe": 1.00,
                    "eps_current_year": 1.00,
                    "eps_forward": 1.00,
                    "eps_trailing_twelve_months": 1.00,
                }
            ],
        }
