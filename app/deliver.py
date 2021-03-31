import requests
import structlog

from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError
from requests.packages.urllib3.exceptions import MaxRetryError
from requests.packages.urllib3.util.retry import Retry
from app import DELIVER_SERVICE_URL


DELIVER_NAME = 'zip'
logger = structlog.get_logger()
session = requests.Session()
retries = Retry(total=5, backoff_factor=0.1)
session.mount('http://', HTTPAdapter(max_retries=retries))


class DeliveryError(Exception):
    pass


def deliver_comments(file_name: str, zip_file: bytes):
    print(logger.name)
    logger.info(logger.name)
    logger.info('Delivering comments')
    file_type = "comments"
    metadata = create_comments_metadata(file_name)
    response = post(zip_file, file_type, metadata)
    status_code = response.status_code

    if status_code == 200:
        logger.info('Successfully delivered comments')
        return True
    elif 400 <= status_code < 500:
        msg = "Bad Request response from sdx-deliver"
        logger.error(msg, status_code=structlog)
        raise Exception(msg)
    else:
        msg = "Bad response from sdx-deliver"
        logger.error(msg, status_code=status_code)
        raise DeliveryError(msg)


def create_comments_metadata(file_name) -> dict:
    metadata = {
        'filename': file_name,
        'tx_id': file_name,
        'survey_id': file_name,
        'description': 'significant changes comments zip',
        'iteration': file_name
    }
    return metadata


def post(file_bytes, file_type, metadata):
    url = f"http://{DELIVER_SERVICE_URL}/deliver/{file_type}"
    logger.info(f"calling {url}")
    try:
        logger.info(f'posting comments to {url}')
        response = session.post(url, params=metadata, files={DELIVER_NAME: file_bytes})
    except MaxRetryError:
        logger.error("Max retries exceeded", request_url=url)
        raise DeliveryError("Max retries exceeded")
    except ConnectionError:
        logger.error("Connection error", request_url=url)
        raise DeliveryError("Connection error")

    return response
