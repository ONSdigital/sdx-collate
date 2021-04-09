import unittest
from unittest.mock import patch, Mock, MagicMock

import app
from app import cloud_config, secret_manager, get_secret
from app.logger import _MaxLevelFilter


class TestInit(unittest.TestCase):

    @patch('app.get_secret')
    @patch('app.pubsub_v1')
    @patch('app.datastore')
    def test_cloud_config(self, mock_datastore, mock_pubsub, mock_get_secret):
        mock_pubsub.SubscriberClient.return_value = Mock()
        ds_client = Mock()
        mock_datastore.Client = ds_client
        cloud_config()
        ds_client.assert_called_with(project=app.project_id)

    @patch('app.get_secret', return_value='my secret')
    @patch('app.datastore')
    def test_cloud_config(self, mock_datastore, mock_secret):
        cloud_config()
        assert app.CONFIG.DECRYPT_COMMENT_KEY == 'my secret'
        assert app.CONFIG.DATASTORE_CLIENT is not None

    def test_logger(self):
        ml = _MaxLevelFilter(4)
        mock_log_record = Mock()
        mock_log_record.levelno = 3
        self.assertTrue(ml.filter(mock_log_record))

    @patch('app.secret_manager.secretmanager')
    def test_secret_manager(self, mock_secret_manager):
        project_id = "test"
        secret = "secret"
        secret_manager.client = MagicMock()
        actual = get_secret(project_id, secret)
        self.assertTrue(actual)
