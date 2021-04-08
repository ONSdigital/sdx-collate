import unittest

from unittest.mock import patch
from app.datastore_connect import fetch_comments
from app import CONFIG


class TestDataStoreConnect(unittest.TestCase):

    @patch('app.datastore_connect.CONFIG')
    @patch('app.datastore_connect.decrypt_comment')
    def test_fetch_comments(self, mock_decrypt_comment, mock_config):
        mock_datastore_client_setup = mock_config.datastore.Client
        mock_datastore_client = mock_datastore_client_setup(project=CONFIG.PROJECT_ID)
        mock_query = mock_datastore_client.query
        mock_fetch = mock_query.fetch.return_value = {
                'Comment': '032dbc9b-ef8c-46cb-b657-8672d3a57320',
                'encrypted_data': 'value',
                'period': '201817',
                'survey': '019'
            }
        fetch_comments()
        mock_fetch.assert_called()
        mock_query.assert_called_with(kind='Comment')
        mock_decrypt_comment.assert_called()



