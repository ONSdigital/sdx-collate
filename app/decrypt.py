import json

from cryptography.fernet import Fernet
from app import CONFIG


def decrypt_comment(comment_token: str) -> dict:
    """
    Decrypts comments returned from Datastore query
    """
    f = Fernet(CONFIG.DECRYPT_COMMENT_KEY)
    comment_bytes = f.decrypt(comment_token.encode())
    return json.loads(comment_bytes.decode())
