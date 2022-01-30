import boto3
import moto
import pytest

AWS_REGION = "us-east-1"


@pytest.fixture
def mock_sns():
    mock_sns = moto.mock_sns()
    mock_sns.start()
    return boto3.client("sns", region_name=AWS_REGION)


@pytest.fixture
def yf_api_msft_stock_quote():
    return {
        "quoteResponse": {
            "result": [
                {
                    "language": "en-US",
                    "region": "US",
                    "quoteType": "EQUITY",
                    "quoteSourceName": "Delayed Quote",
                    "triggerable": True,
                    "currency": "USD",
                    "firstTradeDateMilliseconds": 511108200000,
                    "trailingAnnualDividendYield": 0.007870864,
                    "epsTrailingTwelveMonths": 9.389,
                    "epsForward": 10.69,
                    "epsCurrentYear": 9.34,
                    "priceEpsCurrentYear": 33.004284,
                    "sharesOutstanding": 7496869888,
                    "bookValue": 21.335,
                    "fiftyDayAverage": 324.429,
                    "fiftyDayAverageChange": -16.168976,
                    "fiftyDayAverageChangePercent": -0.04983826,
                    "twoHundredDayAverage": 293.59924,
                    "twoHundredDayAverageChange": 14.660767,
                    "twoHundredDayAverageChangePercent": 0.04993462,
                    "marketCap": 2310985220096,
                    "forwardPE": 28.836298,
                    "priceToBook": 14.44856,
                    "sourceInterval": 15,
                    "exchangeDataDelayedBy": 0,
                    "pageViewGrowthWeekly": 1.7727553,
                    "averageAnalystRating": "1.7 - Buy",
                    "marketState": "CLOSED",
                    "exchange": "NMS",
                    "shortName": "Microsoft Corporation",
                    "longName": "Microsoft Corporation",
                    "messageBoardId": "finmb_21835",
                    "exchangeTimezoneName": "America/New_York",
                    "exchangeTimezoneShortName": "EST",
                    "gmtOffSetMilliseconds": -18000000,
                    "market": "us_market",
                    "esgPopulated": False,
                    "priceHint": 2,
                    "postMarketChangePercent": 0.19788015,
                    "postMarketTime": 1643417999,
                    "postMarketPrice": 308.87,
                    "postMarketChange": 0.60998535,
                    "regularMarketChange": 8.420013,
                    "regularMarketChangePercent": 2.808169,
                    "regularMarketTime": 1643403603,
                    "regularMarketPrice": 308.26,
                    "regularMarketDayHigh": 308.48,
                    "regularMarketDayRange": "294.45 - 308.48",
                    "regularMarketDayLow": 294.45,
                    "regularMarketVolume": 49743698,
                    "regularMarketPreviousClose": 299.84,
                    "bid": 308.85,
                    "ask": 308.65,
                    "bidSize": 10,
                    "askSize": 8,
                    "fullExchangeName": "NasdaqGS",
                    "financialCurrency": "USD",
                    "regularMarketOpen": 300.23,
                    "averageDailyVolume3Month": 32835932,
                    "averageDailyVolume10Day": 57299640,
                    "fiftyTwoWeekLowChange": 84.000015,
                    "fiftyTwoWeekLowChangePercent": 0.3745653,
                    "fiftyTwoWeekRange": "224.26 - 349.67",
                    "fiftyTwoWeekHighChange": -41.410004,
                    "fiftyTwoWeekHighChangePercent": -0.11842595,
                    "fiftyTwoWeekLow": 224.26,
                    "fiftyTwoWeekHigh": 349.67,
                    "dividendDate": 1646870400,
                    "earningsTimestamp": 1643127406,
                    "earningsTimestampStart": 1650884340,
                    "earningsTimestampEnd": 1651233600,
                    "trailingAnnualDividendRate": 2.36,
                    "trailingPE": 32.83204,
                    "tradeable": False,
                    "displayName": "Microsoft",
                    "symbol": "MSFT",
                }
            ],
            "error": None,
        }
    }
