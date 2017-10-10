import unittest
from persistence import *


class TestPersistenceMethods(unittest.TestCase):

    def setUp(self):
        # need path relative from here for test to run
        persistence.pickle_path = '../persistence/dudes.pk'
        persistence.load_dudes()

    def test_persistence(self):
        dude = 00000
        self.assertFalse(persistence.is_dude(dude))

        # Now, he should be a dude
        self.assertTrue(persistence.is_dude(dude))
        persistence.un_dude(dude)

        # Now, he should not be a dude
        self.assertFalse(persistence.is_dude(dude))
        persistence.un_dude(dude)

    def tearDown(self):
        persistence.un_dude(00000)

        # set pickle_path back to normal
        persistence.pickle_path = './persistence/dudes.pk'


if __name__ == '__main__':
    unittest.main()
