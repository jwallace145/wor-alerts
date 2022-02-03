import pytest
from mock import patch
from requests.models import Response
from src.models.stock_quote import StockQuote
from src.yf_api_controller import YFApiController


class TestYFApiController:
    @pytest.fixture(autouse=True)
    def init_test_yf_api_controller(self):
        self.yf_api = YFApiController(api_key="")

    @patch("src.yf_api_controller.requests.models.Response.json")
    @patch("src.yf_api_controller.requests.request", return_value=Response())
    def test_get_stock_quotes(self, mock_request, mock_json, yf_api_msft_stock_quote):
        mock_json.return_value = yf_api_msft_stock_quote
        stock_quotes = self.yf_api.get_stock_quotes(symbols=set("MSFT"))
        assert isinstance(stock_quotes, dict)
        assert isinstance(stock_quotes["MSFT"], StockQuote)
        assert stock_quotes["MSFT"].symbol == "MSFT"
        assert stock_quotes["MSFT"].name == "Microsoft"
        assert stock_quotes["MSFT"].currency == "USD"
        assert stock_quotes["MSFT"].market_price == 308.26
