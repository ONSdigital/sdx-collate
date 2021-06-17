import unittest

from unittest.mock import patch, Mock

from app.datastore_connect import fetch_comment_kinds, fetch_data_for_kind


class MockKeyEntity:

    def __init__(self, key=None) -> None:
        m = Mock()
        m.id_or_name = key
        self.key = m


def mock_data_entity(data):
    return {"encrypted_data": data}


class TestDataStoreConnect(unittest.TestCase):

    @patch('app.datastore_connect.CONFIG')
    def test_fetch_comment_kinds(self, mock_config):
        mock_query = Mock()
        mock_config.DATASTORE_CLIENT.query.return_value = mock_query
        mock_query.fetch.return_value = [
            MockKeyEntity('009_2020'),
            MockKeyEntity('009_2021'),
            MockKeyEntity('023_201817'),
            MockKeyEntity('__non_comment_kind__'),
            MockKeyEntity('__datastore_metadata__')
        ]
        self.assertEqual(['009_2020', '009_2021', '023_201817'], fetch_comment_kinds())

    @patch('app.datastore_connect.CONFIG')
    def test_fetch_comment_kinds_fail(self, mock_config):
        mock_config.DATASTORE_CLIENT.query.return_value = Exception()
        with self.assertRaises(Exception):
            fetch_comment_kinds()

    @patch('app.datastore_connect.CONFIG')
    def test_fetch_data_for_kind(self, mock_config):
        mock_query = Mock()
        mock_config.DATASTORE_CLIENT.query.return_value = mock_query
        mock_query.fetch.return_value = [
            mock_data_entity('12345'),
            mock_data_entity('abcde'),
            mock_data_entity('1a2b3c'),
        ]
        self.assertEqual(['12345', 'abcde', '1a2b3c'], fetch_data_for_kind('009_2020'))

    @patch('app.datastore_connect.CONFIG')
    def test_fetch_data_for_kind_fail(self, mock_config):
        mock_query = Mock()
        mock_config.DATASTORE_CLIENT.query.return_value = mock_query
        with self.assertRaises(Exception):
            fetch_data_for_kind('')
