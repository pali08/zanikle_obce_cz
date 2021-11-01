import unittest

from get_actual_db import create_empty_database_with_coords_as_key, append_to_database_with_coords_as_key, \
    WESTEST_POINT, SOUTHEST_POINT


class MyTestCase(unittest.TestCase):
    def test_create_empty_database_with_coords_as_key(self):
        self.assertEqual(len(create_empty_database_with_coords_as_key(100)), 6768)
        self.assertEqual(len(create_empty_database_with_coords_as_key(100)[0]), 2504)

    empty_list_of_places = create_empty_database_with_coords_as_key(100)

    def test_append_to_database_with_coords_as_key_1(self):
        place = append_to_database_with_coords_as_key(self.empty_list_of_places,
                                                      'http://www.zanikleobce.cz/index.php?obec=26519', sampling=100)
        self.assertEqual(
            place[14549 - int((WESTEST_POINT * 100000) / 100)][50526 - int((SOUTHEST_POINT * 100000) / 100)][0],
            {'name': 'Rozprechtice statek', 'category': 'Dvůr', 'district': 'Česká Lípa',
             'end_reason': 'Nespecifikováno', 'end_years': 'Po 2000', 'actual_state': 'Ohrožená',
             'N': 50.52676, 'E': 14.54951})


if __name__ == '__main__':
    unittest.main()
