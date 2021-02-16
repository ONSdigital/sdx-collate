import os

from app.logger import logging_config
from app.secret_manager import get_secret

logging_config()

PROJECT_ID = os.getenv('PROJECT_ID', 'ons-sdx-sandbox')

DELIVER_SERVICE_URL = "sdx-deliver:80"

DECRYPT_COMMENT_KEY = get_secret(PROJECT_ID, 'sdx-comment-key')
