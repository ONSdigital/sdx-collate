FROM python:3.8-slim
COPY . /app
WORKDIR /app
RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --deploy --ignore-pipfile
CMD ["pipenv", "run", "python", "./run.py"]
