import json
import structlog

from cryptography.fernet import Fernet
from app import DECRYPT_COMMENT_KEY

logger = structlog.get_logger()


def decrypt_comment(comment_token: str) -> dict:
    logger.info(f'Decrypting comment using: {DECRYPT_COMMENT_KEY}')
    f = Fernet(DECRYPT_COMMENT_KEY)
    comment_bytes = f.decrypt(comment_token.encode())
    return json.loads(comment_bytes.decode())
