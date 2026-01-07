import json

from cryptography.fernet import Fernet

from app.submission import CommentData


class Decrypter:

    def __init__(self, decryption_key: str):
        self._decryption_key = decryption_key

    def decrypt_comment(self, comment_token: str) -> CommentData:
        """
        Decrypts comments returned from Datastore query
        """
        f = Fernet(self._decryption_key)
        comment_bytes = f.decrypt(comment_token.encode())
        return json.loads(comment_bytes.decode())
