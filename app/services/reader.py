from datetime import datetime

from sdx_base.services.datastore import DatastoreService

from app import get_logger


logger = get_logger()


class DbReader:

    def __init__(self, project_id: str, datastore_service: DatastoreService):
        self._project_id = project_id
        self._datastore_service = datastore_service

    def fetch_comment_kinds(self) -> list:
        """
            Fetch a list of all comment kinds from datastore.
            Each kind is represented by {survey_id}_{period}
        """
        return self._datastore_service.fetch_kinds(self._project_id)

    def fetch_entity_list(self, kind: str, start_date: datetime, end_date: datetime) -> list:
        """
            Returns a list of the entities for the given 'kind',
            created between start_date (inclusive) and end_date (exclusive).
        """
        return self._datastore_service.fetch_entity_list_for_kind(self._project_id, kind, start_date, end_date)

    def fetch_data_for_kind(self, kind: str, start_date: datetime, end_date: datetime) -> list:
        """
            Returns a list of the encrypted data field from each entity within the given kind
        """
        result_list = []
        entities = self.fetch_entity_list(kind, start_date, end_date)
        for entity in entities:
            result_list.append(entity['encrypted_data'])
        return result_list

    def fetch_data_for_survey(self,
                              survey_id: str,
                              period_list: list[str],
                              start_date: datetime,
                              end_date: datetime) -> dict[str, list]:
        """
            Returns a dict of the encrypted data fields for the given survey mapped to the period
        """
        result_dict = {p: [] for p in period_list}
        for period in period_list:
            entities = self.fetch_entity_list(f'{survey_id}_{period}', start_date, end_date)
            for entity in entities:
                result_dict[period].append(entity['encrypted_data'])
        return result_dict
