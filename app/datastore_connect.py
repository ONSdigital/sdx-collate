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


def fetch_entity_list_for_kind(kind: str) -> list:
    """
        Returns a list of the entities for the given kind
    """
    try:
        if kind is None or kind == '':
            raise Exception(f'Invalid value for kind {kind}')
        query = CONFIG.DATASTORE_CLIENT.query(kind=kind)
        return list(query.fetch())
    except Exception as e:
        logger.error(f'Datastore error fetching entities: {e}')
        print(e)
        raise e


def fetch_data_for_kind(kind: str) -> list:
    """
        Returns a list of the encrypted data field from each entity within the given kind
    """
    result_list = []
    entities = fetch_entity_list_for_kind(kind)
    for entity in entities:
        result_list.append(entity['encrypted_data'])
    return result_list
