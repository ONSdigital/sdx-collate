import unittest

from app.decrypt import decrypt_comment


class TestDecrypt(unittest.TestCase):

    def test_decrypt_comment(self):
        data = '''gAAAAABgCE5W1uIF-eNt96wT7sOOwgQyBoMNWhoGTzt3PZQeBw2LDQDK8oFWJtXW0aWbp4F5li8o8DxdZ2G9Hjq0Y5ahRAhyJj
        xMxAqdg9-Xmm6TKdgzKV9nY6WmnjsllJIrbefIz6vZpZw_IbXgeBILffnWeQDIw4F4s3HiDK37VZCVxuCJLAyRiQjorB5QxxjX7kvzLkwM'''
        actual = decrypt_comment(data)
        print(actual)
        expected = {'ru_ref': '34650525171T',
                    'boxes_selected': '',
                    'comment': 'Yes',
                    'additional': []}
        self.assertEqual(actual, expected)