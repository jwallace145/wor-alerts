import os

import boto3

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

dynamodb = boto3.client("dynamodb", region_name=AWS_REGION)

s3 = boto3.client("s3")

sns = boto3.client("sns", region_name=AWS_REGION)
