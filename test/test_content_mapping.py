import unittest
from util import *


class TestContentMappingMethods(unittest.TestCase):

    def setUp(self):
        return

    def test_listen_to(self):
        response = content_mapping.listen_to("lol, shit")
        self.assertTrue(['', '🍭', False] in response)
        self.assertTrue(['', '💩', False] in response)
        self.assertEqual(content_mapping.listen_to("nothing here"), [])

    def test_mentioned_in(self):
        response0 = content_mapping.mentioned_in("diabetes, bonzi")
        self.assertTrue(['Thankfully, frogs don\'t get diabetes.', '', False] in response0)
        self.assertTrue(['#fuckbonzi', '🅱', False] in response0)

        response1 = content_mapping.mentioned_in("fuck you, diabetes!")
        self.assertTrue(['I\'m sorry you feel that way, my guy', '😢', True] in response1)
        self.assertEqual(len(response1), 1)

        response2 = content_mapping.mentioned_in("nothing here, fellas")
        self.assertEqual(response2, [])

    def tearDown(self):
        return


if __name__ == '__main__':
    unittest.main()
