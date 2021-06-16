import structlog

from datetime import date, datetime
from app import CONFIG
from app.decrypt import decrypt_comment


logger = structlog.get_logger()


def get_kinds() -> list:
    try:
        query = CONFIG.DATASTORE_CLIENT.query(kind="__kind__")
        query.keys_only()
        return [entity.key.id_or_name for entity in query.fetch() if not entity.key.id_or_name.startswith("_")]
    except Exception as e:
        logger.error(f'Datastore: {e}')


def get_data_for_kind(kind: str) -> list:
    try:
        query = CONFIG.DATASTORE_CLIENT.query(kind=kind)
        query.projection = ["encrypted_data"]
        return [entity["encrypted_data"] for entity in query.fetch()]
    except Exception as e:
        logger.error(f'Datastore: {e}')
