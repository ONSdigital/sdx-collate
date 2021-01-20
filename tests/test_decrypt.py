import unittest

from app.decrypt import decrypt_comment


class TestDecrypt(unittest.TestCase):

    def test_decrypt_comment_009(self):
        data = '''gAAAAABgCE5W1uIF-eNt96wT7sOOwgQyBoMNWhoGTzt3PZQeBw2LDQDK8oFWJtXW0aWbp4F5li8o8DxdZ2G9Hjq0Y5ahRAhyJj
        xMxAqdg9-Xmm6TKdgzKV9nY6WmnjsllJIrbefIz6vZpZw_IbXgeBILffnWeQDIw4F4s3HiDK37VZCVxuCJLAyRiQjorB5QxxjX7kvzLkwM'''
        actual = decrypt_comment(data)
        print(actual)
        expected = {'ru_ref': '34650525171T',
                    'boxes_selected': '',
                    'comment': 'Yes',
                    'additional': []}
        self.assertEqual(expected, actual)

    def test_decrypt_comment_187(self):
        data = '''gAAAAABgCE1_ZOqzC9k2ssl9mRBMz1eso1fGkh7r0bO0HTwCkuqXwkTV32nq4syKoctX9SdvqeiMAnIs06ttzZ-9HjNo4sHzH7C4n
        _MXxShKuN9Yy066aBeJU2xVvPPSzSVkt3a7HZOBaNMa-fLB4TRw2T7cdPKAQeD5cK5wAh5Sv0HQkfWH5G25T-nPTcfMbkdQkBICEdOn'''

        actual = decrypt_comment(data)
        print(actual)
        expected = {'ru_ref': '12346789012A',
                    'boxes_selected': '',
                    'comment': None,
                    'additional': []}
        self.assertEqual(expected, actual)