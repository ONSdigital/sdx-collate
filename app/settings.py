from typing import Annotated

from sdx_base.settings.app import AppSettings
from sdx_base.settings.service import SECRET


class Settings(AppSettings):
    deliver_service_url: str = "http://sdx-deliver:80"
    decrypt_comment_key: Annotated[SECRET, "sdx-comment-key"]
