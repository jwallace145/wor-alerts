import csv

import pytest
from src.utils.csv_generator import CsvGenerator

TEST_CSV_FILE_NAME = "testdata.csv"
TEST_WORKING_DIR = "tests/"


class TestCsvGenerator:
    @pytest.fixture(autouse=True)
    def init_test_csv_generator(self):
        self.csv_generator = CsvGenerator(
            file_name="testdata.csv", working_dir="tests/"
        )

    def test_generate_csv(self, mock_users, mock_stock_quotes_dict):
        self.csv_generator.generate_csv(
            users=mock_users, stock_quotes=mock_stock_quotes_dict
        )
        csvreader = csv.reader(open(f"{TEST_WORKING_DIR}{TEST_CSV_FILE_NAME}"))
        headers = next(csvreader)
        data = next(csvreader)
        assert headers == [
            "Email",
            "Stock",
            "Buy Price",
            "Sell Price",
            "Market Price",
            "Trailing PE",
            "Forward PE",
            "EPS Current Year",
            "EPS Forward",
            "EPS Trailing 12 Months",
        ]
        assert data == [
            "testuser1@gmail.com",
            "MSFT",
            "300.0",
            "350.0",
            "305.94",
            "32.58494",
            "28.459536",
            "9.34",
            "10.75",
            "9.389",
        ]
