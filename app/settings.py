from typing import Annotated

from sdx_base.settings.app import AppSettings, get_settings
from sdx_base.settings.service import SECRET


class Settings(AppSettings):
    deliver_service_url: str = "http://sdx-deliver:80"
    decrypt_comment_key: Annotated[SECRET, "sdx-comment-key"]


def get_instance() -> Settings:
    return get_settings(Settings)
