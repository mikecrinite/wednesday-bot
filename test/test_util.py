import unittest
from util import *


class TestUtilMethods(unittest.TestCase):

    def test_my_dudes(self):
        self.assertEqual(util.my_dudes(0), "it is monday, my dudes")

    def test_thanked(self):
        self.assertTrue(util.thanked("thank"))
        self.assertFalse(util.thanked("no thanks"))
        self.assertFalse(util.thanked("angel fish"))

    def test_split(self):
        text0 = 'test_text replace?'
        text1 = 'test-text/#replace'
        text2 = 'test\"text\"%replace'

        self.assertEqual(util.prepare_for_memegen(text0), "test__text_replace~q")
        self.assertEqual(util.prepare_for_memegen(text1), "test--text~s~hreplace")
        self.assertEqual(util.prepare_for_memegen(text2), "test\'\'text\'\'~preplace")

    def test_url_is_valid(self):
        self.assertTrue(util.url_is_valid('https://www.google.com'))  # 200
        self.assertTrue(util.url_is_valid('https://google.com'))      # 301
        self.assertTrue(util.url_is_valid('http://google.com'))      # insecure connections
        self.assertFalse(util.url_is_valid('https://google'))         # 404
        self.assertFalse(util.url_is_valid('https://notaurl'))


if __name__ == '__main__':
    unittest.main()
