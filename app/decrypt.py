import logging

import yaml
from sdc.crypto.key_store import KeyStore
from sdc.crypto.decrypter import decrypt as sdc_decrypt
from structlog import wrap_logger

KEY_PURPOSE_SUBMISSION = 'submission'

logger = wrap_logger(logging.getLogger(__name__))


def decrypt_comment(comment: str) -> dict:
    logger.info("decrypting survey")
    with open("./keys2.yml") as file:
        secrets_from_file = yaml.safe_load(file)
    key_store = KeyStore(secrets_from_file)
    decrypted_json = sdc_decrypt(comment, key_store, KEY_PURPOSE_SUBMISSION)
    logger.info("comment successfully decrypted")
    return decrypted_json
