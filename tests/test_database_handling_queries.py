import unittest

from database_handling_queries import get_distance


class MyTestCase(unittest.TestCase):
    def test_get_distance(self):
        self.assertAlmostEqual(get_distance(52.2296756, 21.0122287, 52.406374, 16.9251681), 279.35290160430094)  # add assertion here


if __name__ == '__main__':
    unittest.main()
