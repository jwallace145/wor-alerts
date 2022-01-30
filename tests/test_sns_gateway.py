import pytest
from src.gateways.sns_gateway import SnsGateway


class TestSnsGateway:
    @pytest.fixture(autouse=True)
    def init_test_sns_gateway(self, mock_sns):
        topic_arn = mock_sns.create_topic(Name="testsnstopic")["TopicArn"]
        self.sns_gateway = SnsGateway(client=mock_sns, topic_arn=topic_arn)

    def test_publish_message(self):
        assert self.sns_gateway.publish_message(message="testmessage") is not None
