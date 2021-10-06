import unittest

from get_data_from_page import get_soup, get_coordinates, get_basic_info, get_other_articles


class MyTestCase(unittest.TestCase):
    soup1 = get_soup('http://www.zanikleobce.cz/index.php?obec=28139')
    soup2 = get_soup('http://www.zanikleobce.cz/index.php?obec=13927')

    def test_coordinates_1(self):
        self.assertEqual(get_coordinates(self.soup1), {'n': 49.35783, 'e': 16.00700})  # add assertion here

    def test_coordinates_2(self):
        self.assertEqual(get_coordinates(self.soup2), {'n': 50.31831, 'e': 12.10138})  # add assertion here

    def test_get_basic_info_1(self):
        self.assertEqual(get_basic_info(self.soup1), {'category': 'Hrad, zámek, tvrz',
                                                      'municipality': 'Lubné - Kutiny',
                                                      'disctrict': 'Brno-venkov',
                                                      'end_reason': 'Nespecifikováno',
                                                      'end_years': 'Před 1945',
                                                      'actual_state': 'Nespecifikováno'
                                                      })

    def test_get_basic_info_2(self):
        self.assertEqual(get_basic_info(self.soup1), {'category': 'Mlýn',
                                                      'municipality': 'Trojmezí',
                                                      'disctrict': 'Cheb',
                                                      'end_reason': 'Hraniční pásmo',
                                                      'end_years': '1945-1950',
                                                      'actual_state': 'Zničena zcela'
                                                      })

    def test_other_articles_1(self):
        self.assertEqual(get_other_articles(self.soup1), 'Žádný záznam')

    def test_other_articles_2(self):
        self.assertEqual(get_other_articles(self.soup1), 'Žádný záznam')


if __name__ == '__main__':
    unittest.main()
