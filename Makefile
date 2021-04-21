build:
	pipenv install
start:
	pipenv run python run.py
test:
	pipenv install --dev ; \
	pytest --cov-report term-missing --cov=app tests/
