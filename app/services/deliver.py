import json
import uuid
from typing import Final, TypedDict, Protocol

import requests

from app import get_logger


FILE_NAME: Final[str] = "filename"
CONTEXT: Final[str] = "context"
TX_ID: Final[str] = "tx_id"
DELIVER_NAME_V2: Final[str] = 'zip_file'
MAX_ATTEMPTS: Final[int] = 3
DELIVER_V2_ENDPOINT: Final[str] = "deliver/v2/comments"

logger = get_logger()


class CommentContext(TypedDict):
    tx_id: str
    survey_type: str
    title: str
    context_type: str


class DeliverHttp(Protocol):
    def post(
        self,
        domain: str,
        endpoint: str,
        json_data: str | None = None,
        params: dict[str, str] | None = None,
        files: dict[str, bytes] | None = None,
    ) -> requests.Response: ...


class DeliverService:

    def __init__(self, deliver_url: str, http_service: DeliverHttp):
        self._deliver_url = deliver_url
        self._http_service = http_service

    def deliver_comments(self, file_name: str, zipped_file: bytes):
        """
        Calls the sdx-deliver endpoint specified by the output_type parameter.
        Returns True or raises appropriate error on response.
        """

        tx_id: str = str(uuid.uuid4())

        context: CommentContext = {
            "tx_id": tx_id,
            "survey_type": "comments",
            "title": "sdx_comments",
            "context_type": "comments_file"
        }

        context_json: str = json.dumps(context)

        self._http_service.post(
            self._deliver_url,
            DELIVER_V2_ENDPOINT,
            None,
            params={FILE_NAME: file_name, TX_ID: tx_id, CONTEXT: context_json},
            files={DELIVER_NAME_V2: zipped_file},
        )
        return True
