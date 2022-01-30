test:
	pipenv run pytest tests --cov=src --cov-report term-missing --verbose

run:
	. ./secrets.sh
	pipenv run python main.py