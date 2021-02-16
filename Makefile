build:
	pip install -r requirements.txt
test:
	pip install -r test_requirements.txt
	python -m pytest
start:
	python run.py
