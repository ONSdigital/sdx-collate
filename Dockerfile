FROM python:3.8-slim
COPY . /app
WORKDIR /app
RUN pip3 install pipenv && pipenv install --deploy --system

ENTRYPOINT ["python3"]
CMD ["run.py"]
