import unittest

from jeopardy.Jeopardy import Jeopardy


class TestPersistenceMethods(unittest.TestCase):

    def setUp(self):
        self.jeopardy = Jeopardy()

    def test_question_incorrect_response(self):
        dude = 00000
        self.jeopardy.get_random_question()
        result = self.jeopardy.response("This is not an answer to any question")
        self.assertEqual(result, [False, "Incorrect"])

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()

