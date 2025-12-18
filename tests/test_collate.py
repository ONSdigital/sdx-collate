import _io
import glob
import json
import logging
import os
import unittest
import zipfile
from datetime import date, timedelta
from pathlib import Path

import pandas

from unittest.mock import patch, Mock

from sdx_base.loggy.configure import BASE_LOGGER_NAME
from sdx_base.run import setup
from sdx_base.services.datastore import DatastoreService
from sdx_base.services.http import HttpService

from app.collate import Collate
from app.definitions.comments import CommentData, DbEntity
from app.services.decrypter import Decrypter
from app.services.deliver import DeliverService
from app.services.reader import DbReader
from app.services.writer import ExcelWriter
from app.settings import Settings
from app.submission import Submission

test_data_009: CommentData = {"ru_ref": "123456", "boxes_selected": "", "comment": "My Comment", "additional": []}

test_data_187: CommentData = {"ru_ref": "123456", "boxes_selected": "91w, 92w1, 92w2", "comment": "I hate covid!",
                 "additional": [
                     {"qcode": "300w", "comment": "I hate covid too!"},
                     {"qcode": "300m", "comment": "I really hate covid!"}]}

test_data_139: CommentData = {"ru_ref": "12346789012A",
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

test_data_134: CommentData = {"ru_ref": "12346789012A",
                 "boxes_selected": "91w, 95w, 96w, 97w, 91f, 95f, 96f, 97f, 191m, 195m, 196m, 197m, 191w4, 195w4, "
                                   "196w4, 197w4, 191w5, 195w5, 196w5, 197w5, ",
                 "comment": "flux clean",
                 "additional": [
                     {"qcode": "300w", "comment": "Pipe \x0B mania"},
                     {"qcode": "300f", "comment": "Gas leak"},
                     {"qcode": "300m", "comment": "copper pipe"},
                     {"qcode": "300w4", "comment": "solder joint"},
                     {"qcode": "300w5", "comment": "drill hole"}
                 ]}


def mock_decrypt(encrypted_data: str) -> CommentData:
    return json.loads(encrypted_data)


class TestCollate(unittest.TestCase):

    def setUp(self):
        proj_root = Path(__file__).parent.parent  # sdx-collate dir
        populated_settings: Settings = setup(Settings, proj_root)
        logger = logging.getLogger(BASE_LOGGER_NAME)
        logger.info(f"Starting {populated_settings.app_name}")

        decrypter: Mock = Mock(spec=Decrypter)
        decrypter.decrypt_comment = mock_decrypt

        self.datastore: Mock = Mock(spec=DatastoreService)
        http_service: HttpService = Mock(spec=HttpService)

        self.collate = Collate(
            reader=DbReader(populated_settings.project_id, datastore_service=self.datastore),
            decrypter=decrypter,
            writer=ExcelWriter(),
            deliver=DeliverService(populated_settings.deliver_service_url, http_service=http_service),
        )

    def tearDown(self):
        files = glob.glob('temp/*')
        for f in files:
            os.remove(f)

    def test_create_zip_verify_009(self):
        self.datastore.fetch_kinds.return_value = ["009_2105", "009_2106"]
        db_entity: DbEntity = {
            "created": "",
            "encrypted_data": json.dumps(test_data_009)
        }
        entity_list: list[str] = [json.dumps(db_entity)]
        self.datastore.fetch_entity_list_for_kind.return_value = entity_list

        yesterday = date.today() - timedelta(1)
        actual = self.collate.create_full_zip(date.today())

        z = zipfile.ZipFile(actual, "r")
        z.extractall('temp')
        daily = pandas.read_excel(f'temp/009_daily_{yesterday}.xlsx')

        self.assertEqual(int(daily.iat[1, 1]), 2105)
        self.assertEqual(daily.iat[1, 3], "My Comment")

        self.assertEqual(int(daily.iat[2, 1]), 2106)
        self.assertEqual(daily.iat[2, 3], "My Comment")

        result_2105 = pandas.read_excel('temp/009_2105.xlsx')
        self.assertEqual(int(result_2105.iat[1, 1]), 2105)
        self.assertEqual(result_2105.iat[1, 3], "My Comment")

        result_2106 = pandas.read_excel('temp/009_2106.xlsx')
        self.assertEqual(int(result_2106.iat[1, 1]), 2106)
        self.assertEqual(result_2106.iat[1, 3], "My Comment")

    @patch('app.collate.fetch_comment_kinds')
    @patch('app.collate.fetch_data_for_kind')
    @patch('app.collate.fetch_data_for_survey')
    def test_create_daily(self, fetch_survey, fetch_data, fetch_kinds):
        fetch_kinds.return_value = ["009_2105", "009_2106"]
        fetch_data.return_value = [test_data_009]
        fetch_survey.return_value = {"2105": [test_data_009], "2106": [test_data_009]}

        today = date.today()
        actual = collate.create_daily_zip_only(today)

        z = zipfile.ZipFile(actual, "r")
        z.extractall('temp')
        result = pandas.read_excel(f'temp/009_daily_{today}.xlsx')

        self.assertEqual(int(result.iat[1, 1]), 2105)
        self.assertEqual(result.iat[1, 3], "My Comment")

        self.assertEqual(int(result.iat[2, 1]), 2106)
        self.assertEqual(result.iat[2, 3], "My Comment")

    @patch('app.collate.fetch_comment_kinds')
    @patch('app.collate.fetch_data_for_kind')
    @patch('app.collate.fetch_data_for_survey')
    def test_create_zip_verify_187(self, fetch_survey, fetch_data, fetch_kinds):
        fetch_kinds.return_value = ["187_201605"]
        fetch_data.return_value = [test_data_187]
        fetch_survey.return_value = {}
        actual = collate.create_full_zip(date.today())
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
        actual = collate.create_full_zip(date.today())
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
    def test_create_zip_134_with_illegal_chars(self, fetch_survey, fetch_data, fetch_kinds):
        fetch_kinds.return_value = ["134_201605"]
        fetch_data.return_value = [test_data_134]
        fetch_survey.return_value = {}
        actual = collate.create_full_zip(date.today())
        self.assertIs(_io.BytesIO, type(actual))

        z = zipfile.ZipFile(actual, "r")
        z.extractall('temp')
        result = pandas.read_excel('temp/134_201605.xlsx')

        self.assertEqual(result.iat[1, 2], '91w, 95w, 96w, 97w, 91f, 95f, 96f, 97f, 191m, 195m, 196m, 197m, 191w4, '
                                           '195w4, 196w4, 197w4, 191w5, 195w5, 196w5, 197w5, ')
        self.assertEqual(result.iat[1, 3], 'flux clean')
        self.assertEqual(result.iat[1, 4], 'This comment contained illegal characters that are not printable')
        self.assertEqual(result.iat[1, 5], 'Gas leak')
        self.assertEqual(result.iat[1, 6], 'copper pipe')
        self.assertEqual(result.iat[1, 7], 'solder joint')
        self.assertEqual(result.iat[1, 8], 'drill hole')
        self.assertEqual(int(result.iat[1, 1]), 201605)
        os.remove('temp/134_201605.xlsx')

    def test_excel_no_comment(self):
        data = [{'ru_ref': '12346789012A', 'boxes_selected': '', 'comment': None, 'additional': []},
                {'ru_ref': '12346789012A', 'boxes_selected': '', 'comment': 'I am a comment', 'additional': []}]
        period = '2105'
        submission_list = [Submission(period, d) for d in data]
        with self.assertLogs('app.excel', level='INFO') as actual:
            create_excel('019', submission_list)

        self.assertEqual(actual.output[1], 'INFO:app.excel:{"logger": "app.excel", "severity": "INFO", "message": "1 '
                                           'out of 2 submissions had comments"}')
