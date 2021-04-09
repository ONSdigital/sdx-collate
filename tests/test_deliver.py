import unittest
from unittest.mock import patch

from requests import exceptions
from requests.packages.urllib3.exceptions import MaxRetryError

from app.deliver import DeliveryError, post


class TestCollate(unittest.TestCase):

    @patch('app.deliver.session')
    def test_post_MaxRetryError(self, mock_session):
        mock_session.post.side_effect = MaxRetryError("pool", "url", "reason")
        with self.assertRaises(DeliveryError):
            post(b"filebytes", "comment", 'metadata')

    @patch('app.deliver.session')
    def test_post_ConnectionError(self, mock_session):
        mock_session.post.side_effect = exceptions.ConnectionError()
        with self.assertRaises(DeliveryError):
            post(b"filebytes", "comment", 'metadata')
