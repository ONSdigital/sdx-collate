FROM eu.gcr.io/ons-sdx-ci/sdx-gcp:1.4.2
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "./run.py"]
