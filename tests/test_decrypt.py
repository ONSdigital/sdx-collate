import unittest

from app.services.decrypter import Decrypter


class TestDecrypt(unittest.TestCase):

    def setUp(self):
        decryption_key = "E3rjFT2i9ALcvc99Pe3YqjIGrzm3LdMsCXc8nUaOEbc="
        self.decrypter = Decrypter(decryption_key)

    def test_decrypt_comment_009(self):
        data = '''gAAAAABgCE5W1uIF-eNt96wT7sOOwgQyBoMNWhoGTzt3PZQeBw2LDQDK8oFWJtXW0aWbp4F5li8o8DxdZ2G9Hjq0Y5ahRAhyJj
        xMxAqdg9-Xmm6TKdgzKV9nY6WmnjsllJIrbefIz6vZpZw_IbXgeBILffnWeQDIw4F4s3HiDK37VZCVxuCJLAyRiQjorB5QxxjX7kvzLkwM'''
        actual = self.decrypter.decrypt_comment(data)

        expected = {'ru_ref': '34650525171T',
                    'boxes_selected': '',
                    'comment': 'Yes',
                    'additional': []}
        self.assertEqual(expected, actual)

    def test_decrypt_comment_187(self):
        data = '''gAAAAABgCE1_ZOqzC9k2ssl9mRBMz1eso1fGkh7r0bO0HTwCkuqXwkTV32nq4syKoctX9SdvqeiMAnIs06ttzZ-9HjNo4sHzH7C4n
        _MXxShKuN9Yy066aBeJU2xVvPPSzSVkt3a7HZOBaNMa-fLB4TRw2T7cdPKAQeD5cK5wAh5Sv0HQkfWH5G25T-nPTcfMbkdQkBICEdOn'''

        actual = self.decrypter.decrypt_comment(data)
        expected = {'ru_ref': '12346789012A',
                    'boxes_selected': '',
                    'comment': None,
                    'additional': []}
        self.assertEqual(expected, actual)

    def test_decrypt_comment_134(self):
        data = '''gAAAAABgHBYKJUU8YTBgSMl4Tv4yl128GLvECa0mIwMkgazY-epsKoUVeIp9QDU2Ya-0FKu-m6Gunfr7xRTKVFsQIiUn8WcJ_vGh
        9eDKVMfU4qoosWrOcIDbIUWjtboGVOF-byXV03cfjvPb8t6Fu6c_z80S8Nm9kHgTu8NTwjo-T_-DkX0rZgBQrKxzBSGkpyEScGb7b6cXg5ZOF
        aX_IV6AyQjcNChwvUji6J3hcOu1eMjpBUXiCty_VsAhn61D0NoSmUuVXPAuUE_wiHWKnsgNtuAz3qeWjjfZrSv09xf3KbXZpIJscUOOCh8fD1
        8-vEc2C_m1csYQe9Ah-HaHxIx8vgFrXEAXJOUG2aP8MdIxwrjlZnXrkodBd_0i6kdYurKS0p12nSf4gzqG06pNcWrnEtLxQltGYuz2TEd2vmxR
        0PfWbd5qQXY8vIXQYniQqHyU_1-MLpJ9jvs7Aupn_Dl1-T2ptFhXpmBoaiDVN5q-Jz3qQDidZJ-MDhfQ4o4aRs9imevVQ-v401QIjnmCsSIXcrz
        tjQnNuAKdVZAB53Ou0L6LR7KcuQ073SiO8zJAnpTWpfmuqYIiAyCD_b0cdpXF2HNrw9Il9J4Em4ATTC2Ii36YQL0TRcLUCbRb9u98KEiTK9FA
        3zzcTVwyKTHGlPC_VCVAD8DpEA=='''

        actual = self.decrypter.decrypt_comment(data)
        expected = {'ru_ref': '12346789012A',
                    'boxes_selected': '91w, 95w, 96w, 97w, 91f, 95f, 96f, 97f, 191m, 195m, 196m, '
                                      '197m, 191w4, 195w4, 196w4, 197w4, 191w5, 195w5, 196w5, '
                                      '197w5, ',
                    'comment': 'flux clean',
                    'additional': [{'comment': 'Pipe mania', 'qcode': '300w'},
                                   {'comment': 'Gas leak', 'qcode': '300f'},
                                   {'comment': 'copper pipe', 'qcode': '300m'},
                                   {'comment': 'solder joint', 'qcode': '300w4'},
                                   {'comment': 'drill hole', 'qcode': '300w5'}]}
        self.assertEqual(expected, actual)
