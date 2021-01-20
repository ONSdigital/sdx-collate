import base64
import json
import logging
from pathlib import Path

from cryptography.fernet import Fernet
from structlog import wrap_logger


logger = wrap_logger(logging.getLogger(__name__))


def decrypt_comment(comment_token: str) -> dict:
    logger.info("decrypting survey")

    key_byte = Path('app/comment_key').read_bytes()
    key = base64.b64encode(key_byte)

    f = Fernet(key)
    comment_bytes = f.decrypt(comment_token.encode())
    return json.loads(comment_bytes.decode())
