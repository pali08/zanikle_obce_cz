import os.path
import sys
import traceback

import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import unquote, urlparse
from pathlib import PurePosixPath

from get_data_from_page import get_data_of_place
from page_download import save_page

url = 'http://www.zanikleobce.cz/index.php?menu=93&sort=1&l=&str=1'
url_main = 'http://www.zanikleobce.cz/'
WESTEST_POINT = 12.09139
EASTEST_POINT = 18.85889
NORTHEST_POINT = 51.05556
SOUTHEST_POINT = 48.55251
DECIMAL_PLACES_COORDS = 100000


# print(table)

def get_number_of_pages():
    url = 'http://www.zanikleobce.cz/index.php?menu=93&sort=1&l=&str=1'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table_lost_places = soup.find('table')
    highest_page = 0
    for tr in table_lost_places.findAll("tr"):
        tds = tr.findAll("td")
        try:
            table_inside = tds[0].find('table')
            for tr in table_inside.findAll('tr'):
                for td in tr.findAll('td'):
                    for div in td.findAll('div'):
                        for link in div.findAll('a'):
                            if 'str=' in link['href']:
                                if int(link['href'].rsplit('str=')[1]) > highest_page:
                                    highest_page = int(link['href'].rsplit('str=')[1])
        except AttributeError as attr_error:
            pass
        except Exception as any_exception:
            print('Exception occurred:' + str(any_exception) + 'stack trace follows')
            print(traceback.format_exc())
    return highest_page


def create_empty_database_with_coords_as_key(sampling):
    eastest = int(((EASTEST_POINT * DECIMAL_PLACES_COORDS) / sampling) + 1)
    westest = int((WESTEST_POINT * DECIMAL_PLACES_COORDS) / sampling)
    northest = int(((NORTHEST_POINT * DECIMAL_PLACES_COORDS) / sampling) + 1)
    southest = int((SOUTHEST_POINT * DECIMAL_PLACES_COORDS) / sampling)
    return [[[] for longitude in range(0, westest-eastest)] for latitude in range(0, northest - southest)]


def append_to_database_with_coords_as_key(list_of_places, web_address, sampling=1):
    data_of_place = get_data_of_place(web_address)
    longitude_index = int(((data_of_place['E']-WESTEST_POINT) * DECIMAL_PLACES_COORDS) / sampling)
    latitude_index = int(((data_of_place['N']-SOUTHEST_POINT) * DECIMAL_PLACES_COORDS) / sampling)
    list_of_places[latitude_index][longitude_index].append(data_of_place)


def get_database_of_lost_places(path, is_test=False):
    if is_test:
        num_of_pages = 1
    else:
        num_of_pages = get_number_of_pages()
    counter = 0
    for i in range(1, num_of_pages + 1):
        url_lost_places = 'http://www.zanikleobce.cz/index.php?menu=93&sort=1&l=&str=' + str(i)
        response = requests.get(url_lost_places)
        soup = BeautifulSoup(response.text, 'html.parser')
        table_lost_places = soup.find('table')
        for tr in table_lost_places.findAll("tr"):
            tds = tr.findAll("td")
            try:
                link = tds[0].find('a')['href']
                if 'obec=' in link:
                    counter += 1
                    session = requests.Session()
                    response = session.get(url_main + link)
                    save_page(response,
                              os.path.join(path, 'item_{:05d}'.format(counter)))
            except AttributeError as attr_error:
                print('attribute error - this should not be problem. Stacktrace follows' + str(attr_error))
            except Exception as any_exception:
                print('Exception occurred:' + str(any_exception) + 'stack trace follows')
                print(traceback.format_exc())


if len(sys.argv) != 2:
    print('1 argument required - path, where to save database of lost places')
else:
    get_database_of_lost_places(sys.argv[1])
