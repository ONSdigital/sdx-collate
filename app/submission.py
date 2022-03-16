
class Submission:

    def __init__(self, period: str, submission_dict: dict):
        self.period = period
        self.comment = submission_dict['comment']
        self.boxes_selected = submission_dict['boxes_selected']
        self.ru_ref = submission_dict['ru_ref']
        self.additional = self._populate_additional(submission_dict)

    @staticmethod
    def _populate_additional(submission_dict) -> dict:
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
