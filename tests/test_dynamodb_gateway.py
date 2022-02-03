import pytest
from src.gateways.dynamodb_gateway import DynamoDbGateway
from mypy_boto3_dynamodb import DynamoDBClient
from src.models.user import User

TEST_STRIKE_PRICES_TABLE_NAME = "test-wor-strike-prices"


class TestDynamoDbGateway:
    @pytest.fixture(autouse=True)
    def init_test_dynamodb_gateway(self, mock_dynamodb: DynamoDBClient):
        mock_dynamodb.create_table(
            AttributeDefinitions=[{"AttributeName": "email", "AttributeType": "S"}],
            TableName=TEST_STRIKE_PRICES_TABLE_NAME,
            KeySchema=[{"AttributeName": "email", "KeyType": "HASH"}],
        )
        mock_dynamodb.put_item(
            TableName=TEST_STRIKE_PRICES_TABLE_NAME,
            Item={
                "phone_number": {"S": "0123456789"},
                "strike_prices": {
                    "L": [
                        {
                            "M": {
                                "symbol": {"S": "MSFT"},
                                "sell_price": {"N": "350"},
                                "buy_price": {"N": "300"},
                            }
                        },
                        {
                            "M": {
                                "symbol": {"S": "AAPL"},
                                "sell_price": {"N": "200"},
                                "buy_price": {"N": "150"},
                            }
                        },
                    ]
                },
                "email": {"S": "testuser@test.com"},
            },
        )
        self.dynamodb_gateway = DynamoDbGateway(
            client=mock_dynamodb, strike_prices_table=TEST_STRIKE_PRICES_TABLE_NAME
        )

    def test_get_users(self):
        users = self.dynamodb_gateway.get_users()
        assert isinstance(users, list)
        assert len(users) == 1
        assert isinstance(users[0], User)
        assert users[0].email == "testuser@test.com"
        assert users[0].phone_number == "0123456789"
        assert len(users[0].strike_prices) == 2
