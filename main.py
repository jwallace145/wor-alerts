import os
from src.yf_api_controller import YFApiController

yf_api = YFApiController(api_key=os.getenv("YF_API_KEY"))

yf_api.get_stock_quote("MSFT")
