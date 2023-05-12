from typing import IO

from sdx_gcp.http import post

from app import CONFIG

DELIVER_NAME = 'zip'


def deliver_comments(file_name: str, zip_file: IO[bytes]):
    """
    Calls the deliver endpoint specified by the output_type parameter.
    Returns True or raises appropriate error on response.
    """
    domain = CONFIG.DELIVER_SERVICE_URL
    endpoint = "deliver/comments"
    post(domain, endpoint, None, params={"filename": file_name}, files={DELIVER_NAME: zip_file})
