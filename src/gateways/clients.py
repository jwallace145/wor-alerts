import os

import boto3

sns = boto3.client("sns", region_name=os.getenv("AWS_REGION", "us-east-1"))
