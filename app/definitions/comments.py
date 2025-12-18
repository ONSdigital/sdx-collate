from datetime import datetime
from typing import TypedDict, Optional


class AdditionalComment(TypedDict):
    qcode: str
    comment: Optional[str]


class CommentData(TypedDict):
    ru_ref: str
    boxes_selected: str
    comment: Optional[str]
    additional: list[AdditionalComment]


class DbEntity(TypedDict):
    created: datetime
    encrypted_data: str
