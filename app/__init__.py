import os

import sdx_gcp.secrets

from google.cloud import datastore
from sdx_gcp.app import get_logger

logger = get_logger()

project_id = os.getenv('PROJECT_ID', 'ons-sdx-sandbox')
deliver_service_url = os.getenv('DELIVER_SERVICE_URL', "http://sdx-deliver:80")


class Config:

    def __init__(self, proj_id) -> None:
        self.PROJECT_ID = proj_id
        self.DECRYPT_COMMENT_KEY = None
        self.DATASTORE_CLIENT = None
        self.DELIVER_SERVICE_URL = deliver_service_url


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
    CONFIG.DECRYPT_COMMENT_KEY = sdx_gcp.secrets.get_secrets(CONFIG.PROJECT_ID, 'sdx-comment-key')[0]
