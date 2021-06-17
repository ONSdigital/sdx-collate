import os
import structlog

from google.cloud import datastore

from app.logger import logging_config
from app.secret_manager import get_secret

logging_config()
logger = structlog.get_logger()

project_id = os.getenv('PROJECT_ID', 'ons-sdx-sandbox')
DELIVER_SERVICE_URL = "sdx-deliver:80"


class Config:

    def __init__(self, proj_id) -> None:
        self.PROJECT_ID = proj_id
        self.DECRYPT_COMMENT_KEY = None
        self.DATASTORE_CLIENT = None


CONFIG = Config(project_id)


def cloud_config():
    """
    Loads configuration required for running against GCP based environments

    This function makes calls to GCP native tools such as Google Secret Manager
    and therefore should not be called in situations where these connections are
    not possible, e.g running the unit tests locally.
    """
    logger.info("Loading Cloud Config")
    datastore_client = datastore.Client(project=CONFIG.PROJECT_ID)
    CONFIG.DATASTORE_CLIENT = datastore_client
    CONFIG.DECRYPT_COMMENT_KEY = get_secret(CONFIG.PROJECT_ID, 'sdx-comment-key')
