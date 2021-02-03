import json
import logging

from cryptography.fernet import Fernet
from structlog import wrap_logger
from app import DECRYPT_COMMENT_KEY


logger = wrap_logger(logging.getLogger(__name__))


def decrypt_comment(comment_token: str) -> dict:
    f = Fernet(DECRYPT_COMMENT_KEY)
    comment_bytes = f.decrypt(comment_token.encode())
    return json.loads(comment_bytes.decode())
