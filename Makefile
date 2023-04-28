build:
	pip install -r requirements.txt
start:
	python run.py
test: build
	pytest -v --cov-report term-missing --disable-warnings --cov=app tests/
