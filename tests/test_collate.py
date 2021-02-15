import _io
import json
import unittest
from unittest.mock import patch

from app.collate import create_zip

test_data = '{"187_201605": [{"ru_ref": "123456", "boxes_selected": "91w, 92w1, 92w2", "comment": "I hate covid!", ' \
            '"additional": [{"qcode": "300w", "comment": "I hate covid too!"}, {"qcode": "300m", "comment": "I really ' \
            'hate covid!"}]}]} '


class TestCollate(unittest.TestCase):

    @patch('app.collate.fetch_comments')
    def test_create_zip(self, fetch_comments):
        pprint.pprint(json.loads(test_data))
        fetch_comments.return_value = json.loads(test_data)
        actual = create_zip()
        self.assertIs(_io.BytesIO, type(actual))
