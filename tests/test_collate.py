import _io
import json
import os
import unittest
import zipfile
import pandas

from requests import Session
from unittest.mock import patch, MagicMock
from app.collate import create_zip, collate_comments
from app.excel import create_excel

test_data = '{"187_201605": [{"ru_ref": "123456", "boxes_selected": "91w, 92w1, 92w2", "comment": "I hate covid!", ' \
            '"additional": [{"qcode": "300w", "comment": "I hate covid too!"}, {"qcode": "300m", "comment": "I really ' \
            'hate covid!"}]}]} '

test_data2 = '{"134_201605": [{"ru_ref": "12346789012A", "boxes_selected": "91w, 95w, 96w, 97w, 91f, 95f, 96f, 97f, ' \
             '191m, 195m, 196m, 197m, 191w4, 195w4, 196w4, 197w4, 191w5, 195w5, 196w5, 197w5, ", "comment": "flux ' \
             'clean", "additional": [{"qcode": "300w", "comment": "Pipe mania"}, {"qcode": "300f", "comment": "Gas ' \
             'leak"}, {"qcode": "300m", "comment": "copper pipe"}, {"qcode": "300w4", "comment": "solder joint"}, ' \
             '{"qcode": "300w5", "comment": "drill hole"}]}]} '


class TestCollate(unittest.TestCase):

    @patch('app.collate.fetch_comments')
    def test_create_zip_type_187(self, fetch_comments):
        fetch_comments.return_value = json.loads(test_data)
        actual = create_zip()
        self.assertIs(_io.BytesIO, type(actual))

    @patch('app.collate.fetch_comments')
    def test_create_zip_verify_187(self, fetch_comments):
        fetch_comments.return_value = json.loads(test_data)
        actual = create_zip()

        z = zipfile.ZipFile(actual, "r")
        z.extractall('temp')
        result = pandas.read_excel('temp/187_201605.xls')

        self.assertEqual(result.iat[1, 3], 'I hate covid!')
        self.assertEqual(result.iat[1, 2], '91w, 92w1, 92w2')
        self.assertEqual(int(result.iat[1, 1]), 201605)
        os.remove('temp/187_201605.xls')

    @patch('app.collate.fetch_comments')
    def test_create_zip_type_134(self, fetch_comments):
        fetch_comments.return_value = json.loads(test_data2)
        actual = create_zip()
        self.assertIs(_io.BytesIO, type(actual))

    @patch('app.collate.fetch_comments')
    def test_create_zip_verify_134(self, fetch_comments):
        fetch_comments.return_value = json.loads(test_data2)
        actual = create_zip()

        z = zipfile.ZipFile(actual, "r")
        z.extractall('temp')
        result = pandas.read_excel('temp/134_201605.xls')

        self.assertEqual(result.iat[1, 2], '91w, 95w, 96w, 97w, 91f, 95f, 96f, 97f, 191m, 195m, 196m, 197m, 191w4, '
                                           '195w4, 196w4, 197w4, 191w5, 195w5, 196w5, 197w5, ')
        self.assertEqual(result.iat[1, 3], 'flux clean')
        self.assertEqual(result.iat[1, 4], 'Pipe mania')
        self.assertEqual(result.iat[1, 5], 'Gas leak')
        self.assertEqual(result.iat[1, 6], 'copper pipe')
        self.assertEqual(result.iat[1, 7], 'solder joint')
        self.assertEqual(result.iat[1, 8], 'drill hole')
        self.assertEqual(int(result.iat[1, 1]), 201605)
        os.remove('temp/134_201605.xls')

    @patch('app.collate.fetch_comments')
    @patch.object(Session, 'post')
    def test_post_400(self, mock_request, mock_fetch):
        with self.assertRaises(Exception):
            mock_fetch.return_value = json.loads(test_data)
            mock_request.return_value.status_code = 400
            collate_comments()

    @patch('app.collate.fetch_comments')
    @patch.object(Session, 'post')
    def test_post_503(self, mock_request, mock_fetch):
        with self.assertLogs('app.deliver', level='ERROR'):
            mock_fetch.return_value = json.loads(test_data)
            mock_request.return_value.status_code = 503
            collate_comments()

    @patch('app.collate.fetch_comments')
    @patch('app.deliver.post')
    def test_post_200(self, mock_post, mock_fetch):
        with self.assertLogs('app.deliver', level='INFO'):
            mock_post_method = MagicMock()
            mock_post_method.status_code = 200
            mock_fetch.return_value = json.loads(test_data)
            mock_post.return_value = mock_post_method
            collate_comments()

    def test_excel_no_comment(self):
        data = [{'ru_ref': '12346789012A', 'boxes_selected': '', 'comment': None, 'additional': []},
                {'ru_ref': '12346789012A', 'boxes_selected': '', 'comment': 'I am a comment', 'additional': []}]
        with self.assertLogs('app.excel', level='INFO') as actual:
            create_excel('019', '20181', data)
        self.assertEqual(actual.output[1], 'INFO:app.excel:{"event": "1 out of 2 submissions had comments", '
                                           '"level": "info", "logger": "app.excel"}')
