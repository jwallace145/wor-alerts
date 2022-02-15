import os

import boto3
from mypy_boto3_dynamodb import DynamoDBClient
from mypy_boto3_sns import SNSClient
from mypy_boto3_s3 import S3Client
from mypy_boto3_ses import SESClient

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

dynamodb: DynamoDBClient = boto3.client("dynamodb", region_name=AWS_REGION)

s3: S3Client = boto3.client("s3")

ses: SESClient = boto3.client("ses", region_name=AWS_REGION)

sns: SNSClient = boto3.client("sns", region_name=AWS_REGION)
