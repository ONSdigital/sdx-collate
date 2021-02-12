import os
import logging

from app.secret_manager import get_secret

LOGGING_LEVEL = logging.getLevelName(os.getenv('LOGGING_LEVEL', 'INFO'))
LOGGING_FORMAT = "%(asctime)s.%(msecs)06dZ|%(levelname)s: sdx-collate: %(message)s"

logging.basicConfig(
    format=LOGGING_FORMAT,
    datefmt="%Y-%m-%dT%H:%M:%S",
    level=LOGGING_LEVEL,
)

PROJECT_ID = os.getenv('PROJECT_ID', 'ons-sdx-sandbox')

DELIVER_SERVICE_URL = "sdx-deliver:80"

DECRYPT_COMMENT_KEY = get_secret(PROJECT_ID, 'sdx-comment-key')
