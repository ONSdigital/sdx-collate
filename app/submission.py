from typing import TypedDict, Optional


class AdditionalComment(TypedDict):
    qcode: str
    comment: Optional[str]


class CommentData(TypedDict):
    ru_ref: str
    boxes_selected: str
    comment: Optional[str]
    additional: list[AdditionalComment]


class Submission:

    def __init__(self, period: str, comment_data: CommentData):
        self.period = period
        self.comment = comment_data['comment']
        self.boxes_selected = comment_data['boxes_selected']
        self.ru_ref = comment_data['ru_ref']
        self.additional = self._populate_additional(comment_data)

    @staticmethod
    def _populate_additional(submission_dict) -> dict[str, str]:
        additional_list = submission_dict['additional']
        additional_dict = {}
        for addition in additional_list:
            additional_dict[addition['qcode']] = addition['comment']
        return additional_dict

    def has_comment(self) -> bool:
        if not self.comment or self.comment == "":
            return False
        else:
            return True
