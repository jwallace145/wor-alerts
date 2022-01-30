import os
from dataclasses import dataclass

from boto3 import Session
from src.gateways.clients import sns


@dataclass
class SnsGateway:

    client: Session = sns
    topic_arn: str = os.getenv("AWS_TOPIC_ARN")

    def publish_message(self, message: str) -> None:
        return self.client.publish(TopicArn=self.topic_arn, Message=message)[
            "MessageId"
        ]
