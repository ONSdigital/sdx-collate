import builtins
import unittest

from unittest.mock import patch, Mock
from app.datastore_connect import fetch_comments


class TestDataStoreConnect(unittest.TestCase):

    @patch('app.datastore_connect.CONFIG')
    @patch('app.datastore_connect.decrypt_comment')
    def test_fetch_comments(self, mock_decrypt_comment, mock_config):
        mock_query = Mock()
        mock_query = mock_config.DATASTORE_CLIENT.query.return_value
        mock_query.fetch.return_value = [{
                'encrypted_data': 'encrypted comment',
                'period': '201817',
                'survey_id': '019'
            }]
        mock_decrypt_comment.return_value = "decrypted comment"

        self.assertEqual({'019_201817': ['decrypted comment']}, fetch_comments())

    @patch('app.datastore_connect.CONFIG')
    @patch('app.datastore_connect.decrypt_comment')
    @patch('app.datastore_connect.fetch_comments')
    def test_fetch_comments_fail(self, mock_append, mock_decrypt_comment, mock_config):
        mock_query = Mock()
        mock_config.DATASTORE_CLIENT.query.return_value = Exception()
        fetch_comments()
        mock_decrypt_comment.assert_not_called()
