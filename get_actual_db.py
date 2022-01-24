import os.path
import pickle
import shutil
import sqlite3
import sys
import traceback
from shutil import copyfile, move

import overpy
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import unquote, urlparse
from pathlib import PurePosixPath

from get_data_from_page import get_data_of_place
from page_download import save_page

url = 'http://www.zanikleobce.cz/index.php?menu=93&sort=1&l=&str=1'
url_main = 'http://www.zanikleobce.cz/'

# way to get bounding box:
# czechia_json = requests.get('https://nominatim.openstreetmap.org/search', params={'q':'czechia', 'format':'json'}).json()[0]['boundingbox']
# WESTEST_POINT = czechia_json[2]
# EASTEST_POINT = czechia_json[3]
# NORTHEST_POINT = czechia_json[1]
# SOUTHEST_POINT = czechia_json[0]

WESTEST_POINT = 12.09139
EASTEST_POINT = 18.85889
NORTHEST_POINT = 51.05556
SOUTHEST_POINT = 48.55251
DECIMAL_PLACES_COORDS = 100000
SAMPLING = 100


def connection_is_ok():
    try:
        requests.get('http://www.zanikleobce.cz/index.php?menu=93&sort=1&l=&str=1')
        return True
    except requests.exceptions.ConnectionError:
        print('Connection could not be established, update will not be performed')
        return False


def backup_db():
    if os.path.exists(os.path.join('.', 'database.db')):
        move(os.path.join('.', 'database.db'), os.path.join('.', 'database.db_bck'))


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
            print(
                'While getting number of pages, attribute error occured - this should not be problem. Stacktrace '
                'follows: ' + str(
                    attr_error))
        except Exception as any_exception:
            print('While getting number of pages, unexpected exception occurred:\n' + str(
                any_exception) + '\nstack trace follows')
            print(traceback.format_exc())
    return highest_page


def get_database_of_lost_places_sqlitedb():
    if not connection_is_ok():
        return
    backup_db()
    num_of_pages = get_number_of_pages()
    con = sqlite3.connect(os.path.join('.', 'database.db'))
    cur = con.cursor()
    cur.execute('''CREATE TABLE database_lost_places 
    (link text primary key, 
    name text, 
    category text,
    municipality text,
    district text, 
    end_reason text, 
    end_years text, 
    actual_state text, 
    north real, 
    east real)''')
    # for i in range(1, 2):
    for i in range(1, num_of_pages + 1):
        url_lost_places = 'http://www.zanikleobce.cz/index.php?menu=93&sort=1&l=&str=' + str(i)
        response = requests.get(url_lost_places)
        soup = BeautifulSoup(response.text, 'html.parser')
        table_lost_places = soup.find('table')
        for tr in table_lost_places.findAll("tr"):
            tds = tr.findAll("td")
            try:
                link_anchor = tds[0].find('a')
                if link_anchor is not None:
                    link_href = link_anchor['href']
                    if 'obec=' in link_href:
                        full_link = url_main + link_href
                        data_of_lost_place = get_data_of_place(full_link)
                        try:
                            cur.execute(
                                "insert into database_lost_places(link, name, category, municipality, district, "
                                "end_reason, "
                                "actual_state, north, east) "
                                "values (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', {}, {})".format(
                                    full_link, data_of_lost_place['name'], data_of_lost_place['category'],
                                    data_of_lost_place['municipality'],
                                    data_of_lost_place['district'], data_of_lost_place['end_reason'],
                                    data_of_lost_place['actual_state'], data_of_lost_place['N'],
                                    data_of_lost_place['E']
                                ))
                            print('temp_output - got data from page: ' + str(link_href))
                        except sqlite3.OperationalError:
                            print('sqlite3.operational error on {}, data_of_lost_place {}, stacktrace folows:'.format(
                                full_link, str(data_of_lost_place)))
                            print(traceback.format_exc())
            except AttributeError as attr_error:
                print('attribute error - this should not be problem. Stacktrace follows: ' + str(attr_error))
            except Exception as any_exception:
                print('Unexpected xception occurred: \n' + str(any_exception) + '\nstack trace follows:\n')
                # print()
                print(traceback.format_exc())
    cur.execute("CREATE INDEX index_north ON database_lost_places (north);")
    cur.execute("CREATE INDEX index_east ON database_lost_places (east);")
    con.commit()
    con.close()
    print('Database update/creation was finished (probably) successfully.'
          'Old database is backed up as database.db_bck. If in doubt (e.g. too many unexpected exceptions occurred), '
          'please replace database.db with database.db_bck')


def get_database_of_lost_places_pages(path, is_test=False):
    if not connection_is_ok():
        return
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
    print('Backup of lost places pages was finished (probably) successfully.')


def get_center_town_coordinates():
    czechia_bbox = [SOUTHEST_POINT, WESTEST_POINT, NORTHEST_POINT, EASTEST_POINT]
    api = overpy.Overpass()
    result = api.query(
        'node["place"~"town|city|village|municipality"](' + str(SOUTHEST_POINT) + ',' + str(WESTEST_POINT) + ',' + str(
            NORTHEST_POINT) + ',' + str(EASTEST_POINT) + ');out;')
    # todo: these 3 values are not to be printed, but added to DB
    for i in result.nodes:
        print(str(i.lat) + str(i.lon) + i.tags['name'])

# if len(sys.argv) == 1:
#     get_database_of_lost_places_sqlitedb()
# elif len(sys.argv) == 2:
#     get_database_of_lost_places_pages(sys.argv[1])
# else:
#     print('0 arguments or 1 argument required - path, where to save database of lost places')
