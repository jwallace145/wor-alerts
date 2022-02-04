import pytest

from src.gateways.s3_gateway import S3Gateway
from freezegun import freeze_time


class TestS3Gateway:
    @pytest.fixture(autouse=True)
    def init_test_s3_gateway(self, mock_s3):
        self.bucket = "testbucket"
        mock_s3.create_bucket(Bucket=self.bucket)
        self.s3_gateway = S3Gateway(client=mock_s3, bucket=self.bucket)

    @freeze_time("2022-01-01")
    def test_upload_file(self, mock_s3):
        self.s3_gateway.upload_file(file_name="./tests/test.txt", key="test.txt")
        assert (
            mock_s3.get_object(Bucket=self.bucket, Key="2022-01-01/test.txt")
            is not None
        )
