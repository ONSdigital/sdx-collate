import _io
import glob
import os
import unittest
import zipfile
import pandas

from requests import Session
from unittest.mock import patch, Mock
from app import collate
from app.excel import create_excel
from app.submission import Submission

test_data_009 = {"ru_ref": "123456", "boxes_selected": "", "comment": "My Comment", "additional": []}

test_data_187 = {"ru_ref": "123456", "boxes_selected": "91w, 92w1, 92w2", "comment": "I hate covid!",
                 "additional": [
                     {"qcode": "300w", "comment": "I hate covid too!"},
                     {"qcode": "300m", "comment": "I really hate covid!"}]}

test_data_139 = {"ru_ref": "12346789012A",
                 "boxes_selected": "91w, 95w, 96w, 97w, 91f, 95f, 96f, 97f, 191m, 195m, 196m, 197m, 191w4, 195w4, "
                                   "196w4, 197w4, 191w5, 195w5, 196w5, 197w5, ",
                 "comment": "flux clean",
                 "additional": [
                     {"qcode": "300w", "comment": "Pipe mania"},
                     {"qcode": "300f", "comment": "Gas leak"},
                     {"qcode": "300m", "comment": "copper pipe"},
                     {"qcode": "300w4", "comment": "solder joint"},
                     {"qcode": "300w5", "comment": "drill hole"}
                 ]}


def mock_decrypt(data):
    return data


collate.decrypt_comment = mock_decrypt


class TestCollate(unittest.TestCase):

    def tearDown(self):
        files = glob.glob('temp/*')
        for f in files:
            os.remove(f)

    @patch('app.collate.fetch_comment_kinds')
    @patch('app.collate.fetch_data_for_kind')
    @patch('app.collate.fetch_data_for_survey')
    def test_create_zip_verify_009_daily(self, fetch_survey, fetch_data, fetch_kinds):
        fetch_kinds.return_value = ["009_2105", "009_2106"]
        fetch_data.return_value = [test_data_009]
        fetch_survey.return_value = {"2105": [test_data_009], "2106": [test_data_009]}

        actual = collate.create_zip()

        z = zipfile.ZipFile(actual, "r")
        z.extractall('temp')
        result = pandas.read_excel('temp/009-daily.xlsx', header=None)

        self.assertEqual(int(result.iat[2, 1]), 2105)
        self.assertEqual(result.iat[2, 3], "My Comment")

        self.assertEqual(int(result.iat[3, 1]), 2106)
        self.assertEqual(result.iat[3, 3], "My Comment")

    @patch('app.collate.fetch_comment_kinds')
    @patch('app.collate.fetch_data_for_kind')
    @patch('app.collate.fetch_data_for_survey')
    def test_create_zip_verify_187(self, fetch_survey, fetch_data, fetch_kinds):
        fetch_kinds.return_value = ["187_201605"]
        fetch_data.return_value = [test_data_187]
        fetch_survey.return_value = {}
        actual = collate.create_zip()
        self.assertIs(_io.BytesIO, type(actual))

        z = zipfile.ZipFile(actual, "r")
        z.extractall('temp')
        result = pandas.read_excel('temp/187_201605.xlsx')

        self.assertEqual(result.iat[1, 3], 'I hate covid!')
        self.assertEqual(result.iat[1, 2], '91w, 92w1, 92w2')
        self.assertEqual(int(result.iat[1, 1]), 201605)
        os.remove('temp/187_201605.xlsx')

    @patch('app.collate.fetch_comment_kinds')
    @patch('app.collate.fetch_data_for_kind')
    @patch('app.collate.fetch_data_for_survey')
    def test_create_zip_verify_134(self, fetch_survey, fetch_data, fetch_kinds):
        fetch_kinds.return_value = ["134_201605"]
        fetch_data.return_value = [test_data_139]
        fetch_survey.return_value = {}
        actual = collate.create_zip()
        self.assertIs(_io.BytesIO, type(actual))

        z = zipfile.ZipFile(actual, "r")
        z.extractall('temp')
        result = pandas.read_excel('temp/134_201605.xlsx')

        self.assertEqual(result.iat[1, 2], '91w, 95w, 96w, 97w, 91f, 95f, 96f, 97f, 191m, 195m, 196m, 197m, 191w4, '
                                           '195w4, 196w4, 197w4, 191w5, 195w5, 196w5, 197w5, ')
        self.assertEqual(result.iat[1, 3], 'flux clean')
        self.assertEqual(result.iat[1, 4], 'Pipe mania')
        self.assertEqual(result.iat[1, 5], 'Gas leak')
        self.assertEqual(result.iat[1, 6], 'copper pipe')
        self.assertEqual(result.iat[1, 7], 'solder joint')
        self.assertEqual(result.iat[1, 8], 'drill hole')
        self.assertEqual(int(result.iat[1, 1]), 201605)
        os.remove('temp/134_201605.xlsx')

    @patch('app.collate.fetch_comment_kinds')
    @patch('app.collate.fetch_data_for_kind')
    @patch('app.collate.fetch_data_for_survey')
    @patch.object(Session, 'post')
    def test_post_400(self, mock_request, fetch_survey, fetch_data, fetch_kinds):
        with self.assertRaises(Exception):
            fetch_kinds.return_value = ["134_201605"]
            fetch_data.return_value = [test_data_139]
            fetch_survey.return_value = {}
            mock_request.return_value.status_code = 400
            collate.collate_comments()

    @patch('app.collate.fetch_comment_kinds')
    @patch('app.collate.fetch_data_for_kind')
    @patch('app.collate.fetch_data_for_survey')
    @patch.object(Session, 'post')
    def test_post_503(self, mock_request, fetch_survey, fetch_data, fetch_kinds):
        with self.assertLogs('app.deliver', level='ERROR'):
            fetch_kinds.return_value = ["134_201605"]
            fetch_data.return_value = [test_data_139]
            fetch_survey.return_value = {}
            mock_request.return_value.status_code = 503
            collate.collate_comments()

    @patch('app.collate.fetch_comment_kinds')
    @patch('app.collate.fetch_data_for_kind')
    @patch('app.collate.fetch_data_for_survey')
    @patch('app.deliver.post')
    def test_post_200(self, mock_post, fetch_survey, fetch_data, fetch_kinds):
        with self.assertLogs('app.deliver', level='INFO'):
            fetch_kinds.return_value = ["134_201605"]
            fetch_data.return_value = [test_data_139]
            fetch_survey.return_value = {}
            mock_post_method = Mock()
            mock_post_method.status_code = 200
            mock_post.return_value = mock_post_method
            collate.collate_comments()

    def test_excel_no_comment(self):
        data = [{'ru_ref': '12346789012A', 'boxes_selected': '', 'comment': None, 'additional': []},
                {'ru_ref': '12346789012A', 'boxes_selected': '', 'comment': 'I am a comment', 'additional': []}]
        period = '2105'
        submission_list = [Submission(period, d) for d in data]
        with self.assertLogs('app.excel', level='INFO') as actual:
            create_excel('019', submission_list)
        self.assertEqual(actual.output[1], 'INFO:app.excel:{"event": "1 out of 2 submissions had comments", '
                                           '"level": "info", "logger": "app.excel"}')
