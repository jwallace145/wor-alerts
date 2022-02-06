import os
from dataclasses import dataclass

from mypy_boto3_sns import SNSClient
from src.aws_gateways.clients import sns


@dataclass
class SnsGateway:

    client: SNSClient = sns
    topic_arn: str = os.getenv("AWS_TOPIC_ARN")

    def publish_message(self, message: str) -> None:
        return self.client.publish(TopicArn=self.topic_arn, Message=message)[
            "MessageId"
        ]
