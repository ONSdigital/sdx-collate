import json
import time
import uuid
from typing import IO, Final, TypedDict

from sdx_gcp.app import get_logger
from sdx_gcp.errors import RetryableError
from sdx_gcp.http import post

from app import CONFIG

logger = get_logger()

DELIVER_NAME: Final[str] = 'zip'
DELIVER_NAME_V2: Final[str] = 'zip_file'
MAX_ATTEMPTS = 3
DELIVER_V1_ENDPOINT: Final[str] = "deliver/comments"
DELIVER_V2_ENDPOINT: Final[str] = "deliver/v2/comments"
SERVICE_DOMAIN: Final[str] = CONFIG.DELIVER_SERVICE_URL


class CommentContext(TypedDict):
    tx_id: str
    survey_type: str
    title: str


def deliver_comments(file_name: str, zip_file: IO[bytes], attempt: int = 0):
    if CONFIG.PROJECT_ID == "ons-sdx-preprod" or CONFIG.PROJECT_ID == "ons-sdx-nifi":
        deliver_v2_comments(file_name, zip_file, attempt)
    else:
        deliver_v1_comments(file_name, zip_file, attempt)


def deliver_v1_comments(file_name: str, zip_file: IO[bytes], attempt: int = 0):
    """
    Calls the 'deliver' endpoint specified by the output_type parameter.
    Returns True or raises appropriate error on response.
    """

    try:
        post(SERVICE_DOMAIN, DELIVER_V1_ENDPOINT, None, params={"filename": file_name}, files={DELIVER_NAME: zip_file})

    except RetryableError as e:
        logger.error("Failed to deliver comments", error=str(e))
        time.sleep(5)
        if attempt < MAX_ATTEMPTS:
            deliver_v1_comments(file_name, zip_file, attempt + 1)
        else:
            raise e


def deliver_v2_comments(file_name: str, zip_file: IO[bytes], attempt: int = 0):
    """
    Calls the 'deliver' endpoint specified by the output_type parameter.
    Returns True or raises appropriate error on response.
    """

    tx_id: str = str(uuid.uuid4())

    context: CommentContext = {
        "tx_id": tx_id,
        "survey_type": "comments",
        "title": "sdx_comments",
        "context_type": "comments_file"
    }

    try:
        post(SERVICE_DOMAIN, DELIVER_V2_ENDPOINT, None, params={"filename": file_name, "context": json.dumps(context),
                                                                "tx_id": tx_id}, files={DELIVER_NAME_V2: zip_file})

    except RetryableError as e:
        logger.error("Failed to deliver comments", error=str(e))
        time.sleep(5)
        if attempt < MAX_ATTEMPTS:
            deliver_v2_comments(file_name, zip_file, attempt + 1)
        else:
            raise e
