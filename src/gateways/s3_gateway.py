import os
from dataclasses import dataclass

from mypy_boto3_s3 import S3Client
from src.gateways.clients import s3
from src.utils.logger import Logger

log = Logger(__name__).get_logger()


@dataclass
class S3Gateway:

    client: S3Client = s3
    bucket: str = os.getenv("AWS_BUCKET")

    def upload_file(self, file_name: str, key: str) -> None:
        log.info(
            f"Uploading {file_name} to S3 bucket {self.bucket} with key {key}....."
        )
        self.client.upload_file(Filename=file_name, Bucket=self.bucket, Key=key)
