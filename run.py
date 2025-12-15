import logging
from pathlib import Path

from sdx_base.loggy.configure import BASE_LOGGER_NAME
from sdx_base.run import setup
from sdx_base.settings.app import AppSettings
from app.collate import collate_comments
from app.settings import Settings


if __name__ == '__main__':
    proj_root = Path(__file__).parent  # sdx-collate dir
    populated_settings: AppSettings = setup(Settings, proj_root)
    logger = logging.getLogger(BASE_LOGGER_NAME)
    logger.info(f"Starting {populated_settings.app_name}")
    collate_comments()
