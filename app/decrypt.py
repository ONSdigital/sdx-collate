import json
import logging
from pathlib import Path

from cryptography.fernet import Fernet
from structlog import wrap_logger


logger = wrap_logger(logging.getLogger(__name__))


def decrypt_comment(comment_token: str) -> dict:
    logger.info("decrypting survey")
    key = Path('comment_key.txt').read_bytes()
    f = Fernet(key)
    comment_bytes = f.decrypt(comment_token.encode())
    return json.loads(comment_bytes.decode())
