import logging
from pathlib import Path

from sdx_base.loggy.configure import BASE_LOGGER_NAME
from sdx_base.run import setup
from sdx_base.services.datastore import DatastoreService
from sdx_base.services.http import HttpService

from app.collate import Collate
from app.services.decrypter import Decrypter
from app.services.deliver import DeliverService
from app.services.reader import DbReader
from app.services.writer import ExcelWriter
from app.settings import Settings


if __name__ == '__main__':
    proj_root = Path(__file__).parent  # sdx-collate dir
    populated_settings: Settings = setup(Settings, proj_root)
    logger = logging.getLogger(BASE_LOGGER_NAME)
    logger.info(f"Starting {populated_settings.app_name}")

    collate = Collate(
        reader=DbReader(populated_settings.project_id, datastore_service=DatastoreService()),
        decrypter=Decrypter(decryption_key=populated_settings.decrypt_comment_key),
        writer=ExcelWriter(),
        deliver=DeliverService(deliver_url=populated_settings.deliver_service_url, http_service=HttpService()),
    )
    collate.collate_comments()
