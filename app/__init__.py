import os

from google.cloud import datastore

from app.logger import logging_config
from app.secret_manager import get_secret

logging_config()

project_id = os.getenv('PROJECT_ID', 'ons-sdx-sandbox')
DELIVER_SERVICE_URL = "sdx-deliver:80"


class Config:

    def __init__(self, proj_id) -> None:
        self.PROJECT_ID = proj_id
        self.DECRYPT_COMMENT_KEY = "E3rjFT2i9ALcvc99Pe3YqjIGrzm3LdMsCXc8nUaOEbc="
        self.DATASTORE_CLIENT = None


CONFIG = Config(project_id)


def cloud_config():
    datastore_client = datastore.Client(project=CONFIG.PROJECT_ID)
    CONFIG.DATASTORE_CLIENT = datastore_client
    CONFIG.DECRYPT_COMMENT_KEY = get_secret(CONFIG.PROJECT_ID, 'sdx-comment-key')
