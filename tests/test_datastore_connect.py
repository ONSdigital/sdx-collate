import unittest
from datetime import date, datetime

from unittest.mock import patch, Mock

from app.datastore_connect import fetch_data_for_kind, fetch_data_for_survey


class MockKeyEntity:

    def __init__(self, key=None) -> None:
        m = Mock()
        m.id_or_name = key
        self.key = m


def mock_data_entity(data):
    return {"encrypted_data": data}


def mock_date() -> datetime:
    d = date.today()
    return datetime(d.year, d.month, d.day)


class TestDataStoreConnect(unittest.TestCase):

    @patch('app.datastore_connect.fetch_entity_list')
    def test_fetch_data_for_kind(self, mock_fetch):
        mock_fetch.return_value = [
            mock_data_entity('12345'),
            mock_data_entity('abcde'),
            mock_data_entity('1a2b3c'),
        ]
        self.assertEqual(
            ['12345', 'abcde', '1a2b3c'],
            fetch_data_for_kind('009_2020', mock_date(), mock_date()))

    @patch('app.datastore_connect.fetch_entity_list')
    def test_fetch_data_for_survey(self, mock_fetch):

        def fetch_entities(kind: str, start_date: datetime, end_date: datetime):
            if kind == "009_2107":
                return [
                    mock_data_entity('12345'),
                    mock_data_entity('23456'),
                    mock_data_entity('34567')
                ]
            if kind == "009_2108":
                return [
                    mock_data_entity('abcde'),
                    mock_data_entity('bcdef')
                ]
            if kind == "009_2109":
                return [
                    mock_data_entity('1a2b3')
                ]

        mock_fetch.side_effect = fetch_entities
        period_list = ['2107', '2108', '2109']
        expected = {
            '2107': ['12345', '23456', '34567'],
            '2108': ['abcde', 'bcdef'],
            '2109': ['1a2b3'],
        }
        actual = fetch_data_for_survey('009', period_list, mock_date(), mock_date())
        self.assertDictEqual(expected, actual)
