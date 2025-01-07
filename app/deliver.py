import time
from typing import IO

from sdx_gcp.app import get_logger
from sdx_gcp.errors import RetryableError
from sdx_gcp.http import post

from app import CONFIG

logger = get_logger()

DELIVER_NAME = 'zip'
MAX_ATTEMPTS = 3


def deliver_comments(file_name: str, zip_file: IO[bytes], attempt: int = 0):
    """
    Calls the 'deliver' endpoint specified by the output_type parameter.
    Returns True or raises appropriate error on response.
    """
    domain = CONFIG.DELIVER_SERVICE_URL
    endpoint = "deliver/comments"

    try:
        post(domain, endpoint, None, params={"filename": file_name}, files={DELIVER_NAME: zip_file})

    except RetryableError as e:
        logger.error("Failed to deliver comments", error=str(e))
        time.sleep(5)
        if attempt < MAX_ATTEMPTS:
            deliver_comments(file_name, zip_file, attempt + 1)
        else:
            raise e
