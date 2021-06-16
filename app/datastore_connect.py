import structlog

from app import CONFIG


logger = structlog.get_logger()


def fetch_comment_kinds() -> list:
    """
        Fetch a list of all comment kinds from datastore.
        Each kind is represented by {survey_id}_{period}
    """
    try:
        query = CONFIG.DATASTORE_CLIENT.query(kind="__kind__")
        query.keys_only()
        return [entity.key.id_or_name for entity in query.fetch() if not entity.key.id_or_name.startswith("_")]
    except Exception as e:
        logger.error(f'Datastore error fetching kinds: {e}')
        raise e


def fetch_data_for_kind(kind: str) -> list:
    """
        Returns a list of the encrypted data field from each entity within the given kind
    """
    try:
        if kind is None or kind == '':
            raise Exception(f'Invalid value for kind {kind}')
        query = CONFIG.DATASTORE_CLIENT.query(kind=kind)
        query.projection = ["encrypted_data"]
        return [entity["encrypted_data"] for entity in query.fetch()]
    except Exception as e:
        logger.error(f'Datastore error fetching data: {e}')
        print(e)
        raise e
