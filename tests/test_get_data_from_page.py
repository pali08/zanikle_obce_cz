import unittest

import pytest as pytest

from get_data_from_page import get_soup, get_coordinates, get_basic_info, get_data_of_place


class MyTestCase(unittest.TestCase):
    soup1 = get_soup('http://www.zanikleobce.cz/index.php?obec=28139')
    soup2 = get_soup('http://www.zanikleobce.cz/index.php?obec=13927')

    def test_coordinates_1(self):
        self.assertEqual(get_coordinates(self.soup1), {'N': 49.35783, 'E': 16.00700})  # add assertion here

    def test_coordinates_2(self):
        self.assertEqual(get_coordinates(self.soup2), {'N': 50.31831, 'E': 12.10138})  # add assertion here

    def test_get_basic_info_1(self):
        self.assertEqual(get_basic_info(self.soup1), {'name': 'Kuťův mlýn',
                                                      'category': 'Hrad, zámek, tvrz',
                                                      'municipality': 'Lubné - Kutiny',
                                                      'district': 'Brno-venkov',
                                                      'end_reason': 'Nespecifikováno',
                                                      'end_years': 'Před 1945',
                                                      'actual_state': 'Nespecifikováno'
                                                      })

    def test_get_basic_info_2(self):
        self.assertEqual(get_basic_info(self.soup2), {'name': 'Dolní mlýn',
                                                      'category': 'Mlýn',
                                                      'municipality': 'Trojmezí',
                                                      'district': 'Cheb',
                                                      'end_reason': 'Hraniční pásmo',
                                                      'end_years': '1945-1950',
                                                      'actual_state': 'Zničena zcela'
                                                      })

    def test_get_data_of_place_1(self):
        self.assertEqual(get_data_of_place('http://www.zanikleobce.cz/index.php?obec=28139'), {'name': 'Kuťův mlýn',
                                                                                               'category': 'Hrad, zámek, tvrz',
                                                                                               'municipality': 'Lubné - Kutiny',
                                                                                               'district': 'Brno-venkov',
                                                                                               'end_reason': 'Nespecifikováno',
                                                                                               'end_years': 'Před 1945',
                                                                                               'actual_state': 'Nespecifikováno',
                                                                                               'N': 49.35783,
                                                                                               'E': 16.00700
                                                                                               })

    def test_get_data_of_place_2(self):
        self.assertEqual(get_data_of_place('http://www.zanikleobce.cz/index.php?obec=13927'), {'name': 'Dolní mlýn',
                                                                                               'category': 'Mlýn',
                                                                                               'municipality': 'Trojmezí',
                                                                                               'district': 'Cheb',
                                                                                               'end_reason': 'Hraniční pásmo',
                                                                                               'end_years': '1945-1950',
                                                                                               'actual_state': 'Zničena zcela',
                                                                                               'N': 50.31831,
                                                                                               'E': 12.10138})

        if __name__ == '__main__':
            unittest.main()
