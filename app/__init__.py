import os
import logging


LOGGING_LEVEL = logging.getLevelName(os.getenv('LOGGING_LEVEL', 'INFO'))
LOGGING_FORMAT = "%(asctime)s.%(msecs)06dZ|%(levelname)s: sdx-collate: %(message)s"

logging.basicConfig(
    format=LOGGING_FORMAT,
    datefmt="%Y-%m-%dT%H:%M:%S",
    level=LOGGING_LEVEL,
)

PROJECT_ID = os.getenv('PROJECT_ID', 'ons-sdx-sandbox')

DELIVER_SERVICE_HOST = os.getenv('SDX_DELIVER_SERVICE_HOST', 'localhost')
DELIVER_SERVICE_PORT = os.getenv('SDX_DELIVER_SERVICE_PORT', 8080)
DELIVER_SERVICE_URL = f'{DELIVER_SERVICE_HOST}:{DELIVER_SERVICE_PORT}'

# DELIVER_SERVICE_URL = "sdx-deliver:80"
