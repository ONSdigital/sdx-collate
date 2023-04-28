from datetime import datetime
from typing import List

from sdx_gcp.app import get_logger
from sdx_gcp.datastore import fetch_kinds, fetch_entity_list_for_kind


from app import CONFIG


logger = get_logger()


def fetch_comment_kinds() -> list:
    """
        Fetch a list of all comment kinds from datastore.
        Each kind is represented by {survey_id}_{period}
    """
    return fetch_kinds(CONFIG.PROJECT_ID)


def fetch_entity_list(kind: str, start_date: datetime, end_date: datetime) -> list:
    """
        Returns a list of the entities for the given 'kind',
        created between start_date (inclusive) and end_date (exclusive).
    """
    return fetch_entity_list_for_kind(CONFIG.PROJECT_ID, kind, start_date, end_date)


def fetch_data_for_kind(kind: str, start_date: datetime, end_date: datetime) -> list:
    """
        Returns a list of the encrypted data field from each entity within the given kind
    """
    result_list = []
    entities = fetch_entity_list(kind, start_date, end_date)
    for entity in entities:
        result_list.append(entity['encrypted_data'])
    return result_list


def fetch_data_for_survey(survey_id: str, period_list: List[str], start_date: datetime, end_date: datetime) -> dict:
    """
        Returns a dict of the encrypted data fields for the given survey mapped to the period
    """
    result_dict = {p: [] for p in period_list}
    for period in period_list:
        entities = fetch_entity_list(f'{survey_id}_{period}', start_date, end_date)
        for entity in entities:
            result_dict[period].append(entity['encrypted_data'])
    return result_dict
