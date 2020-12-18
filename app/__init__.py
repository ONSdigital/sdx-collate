import os
import logging


LOGGING_LEVEL = logging.getLevelName(os.getenv('LOGGING_LEVEL', 'INFO'))
LOGGING_FORMAT = "%(asctime)s.%(msecs)06dZ|%(levelname)s: sdx-collate: %(message)s"

logging.basicConfig(
    format=LOGGING_FORMAT,
    datefmt="%Y-%m-%dT%H:%M:%S",
    level=LOGGING_LEVEL,
)

PROJECT = 'ons-sdx-sandbox'
