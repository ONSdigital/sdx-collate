import unittest

from app.collate import collate_comments

submission1 = {
    "ru_ref": "123456",
    "boxes_selected": "91w, 92w1, 92w2",
    "comment": "I hate covid!",
    "additional": [
        {"qcode": "300w", "comment": "I hate covid!"},
        {"qcode": "300m", "comment": "I really hate covid!"}
    ]
}

submission2 = {
    "ru_ref": "123456",
    "boxes_selected": "146f 146h",
    "comment": "my comment",
    "additional": []
}


class TestCollate(unittest.TestCase):

    def test_create_xls(self):
        result = collate_comments()
        print(result)
