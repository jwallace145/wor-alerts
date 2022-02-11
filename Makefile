test:
	pipenv run pytest tests --cov=src --cov-report term-missing --verbose

run:
	. ./secrets.sh
	pipenv run python test_local.py

lint:
	pipenv run flake8 --count --max-complexity=10 --max-line-length=127 --show-source --statistics --ignore=E501,W503

format:
	pipenv run black .