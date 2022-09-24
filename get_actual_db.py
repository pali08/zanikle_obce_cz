import csv
import os.path
import pickle
import shutil
import sqlite3
import sys
import traceback
from io import StringIO
from shutil import copyfile, move
from time import sleep

import overpy
import requests
import pandas as pd
import urllib3.exceptions
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
    last_page_link = soup.find('table').find('table').find('tr').find('td').findNext('td').findNext('td') \
        .find('div').findAll('a', recursive=False)[-1]
    return int(last_page_link.text)


def get_table_of_lost_places_sqlitedb():
    if not connection_is_ok():
        return
    backup_db()
    num_of_pages = get_number_of_pages()
    con = sqlite3.connect(os.path.join('.', 'database.db'))
    cur = con.cursor()
    cur.execute('''CREATE TABLE database_lost_places 
    (link text primary key,
    id integer  
    name text, 
    category text,
    municipality text,
    district text, 
    end_reason text, 
    end_years text, 
    actual_state text, 
    north real, 
    east real)''')
    # for i in range(1, 3):
    for i in range(1, num_of_pages + 1):
        url_lost_places = 'http://www.zanikleobce.cz/index.php?menu=93&sort=1&l=&str=' + str(i)
        response = requests.get(url_lost_places)
        soup = BeautifulSoup(response.text, 'html.parser')
        table_lost_places = soup.find('table').find('table').find('table')
        for tr in table_lost_places.findAll("tr")[2:]:
            full_link = url_main + tr.find('td').find('a')['href']
            place_id = int(full_link.split('=')[-1])
            try:
                data_of_lost_place = get_data_of_place(full_link)
                cur.execute(
                    "insert into database_lost_places(link, id, name, category, municipality, district, "
                    "end_reason, end_years"
                    "actual_state, north, east) "
                    "values (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', {}, {})".format(
                        full_link, place_id, data_of_lost_place['name'], data_of_lost_place['category'],
                        data_of_lost_place['municipality'],
                        data_of_lost_place['district'], data_of_lost_place['end_reason'],
                        data_of_lost_place['end_years'],
                        data_of_lost_place['actual_state'], data_of_lost_place['N'],
                        data_of_lost_place['E']
                    ))
                # print('temp_output - got data from page: ' + str(full_link))
            except urllib3.exceptions.NewConnectionError:
                sleep(30)
                continue
            except urllib3.exceptions.MaxRetryError:
                sleep(30)
                continue
            except urllib3.exceptions.ProtocolError:
                sleep(30)
                continue
            except ConnectionResetError:
                sleep(30)
                continue
    cur.execute("CREATE INDEX index_north ON database_lost_places (north);")
    cur.execute("CREATE INDEX index_east ON database_lost_places (east);")
    con.commit()
    con.close()
    print('Database update/creation was finished (probably) successfully.'
          'Old database is backed up as database.db_bck. If in doubt (e.g. too many unexpected exceptions occurred), '
          'please replace database.db with database.db_bck')


def get_table_of_lost_places_pages(path, is_test=False):
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
    csv_towns = requests.get('https://raw.githubusercontent.com/33bcdd/souradnice-mest/master/souradnice.csv').text
    con = sqlite3.connect(os.path.join('.', 'database.db'))
    cur = con.cursor()
    cur.execute('''DROP TABLE IF EXISTS towns_with_coordinates''')
    cur.execute('''CREATE TABLE IF NOT EXISTS towns_with_coordinates
    (town text,
    code text,
    district text,
    district_code text,
    region text,
    region_code text,
    postal_code text,
    north real,
    east real)''')
    csv_file_handle = StringIO(csv_towns)
    csv_towns_reader = csv.reader(csv_file_handle, delimiter=',')
    next(csv_towns_reader)  # remove first line
    for row in csv_towns_reader:
        # print(i.tags)
        # print(str(i.lat) + str(i.lon) + i.tags['name'])
        # print(row)
        try:
            cur.execute(
                "insert into towns_with_coordinates(town,code,district,district_code,region,"
                "region_code,postal_code,north,east)"
                "values (\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',{}, {})".format(*row))
        except sqlite3.OperationalError:
            print('sqlite3.operational error on {}, stacktrace folows:'.format(
                str(row)))
            print(traceback.format_exc())
    cur.execute("CREATE INDEX towns ON towns_with_coordinates (town);")
    con.commit()
    con.close()

# getting town coordinates from overpass
# def get_center_town_coordinates():
#     czechia_bbox = [SOUTHEST_POINT, WESTEST_POINT, NORTHEST_POINT, EASTEST_POINT]
#     api = overpy.Overpass()
#     result = api.query(
#         'node["place"~"town|city|village|municipality"](' + str(SOUTHEST_POINT) + ',' +
#         str(WESTEST_POINT) + ',' + str(
#             NORTHEST_POINT) + ',' + str(EASTEST_POINT) + ');out;')
#     # todo: these 3 values are not to be printed, but added to DB
#
#     con = sqlite3.connect(os.path.join('.', 'database.db'))
#     cur = con.cursor()
#     cur.execute('''DROP TABLE towns_with_coordinates''')
#     cur.execute('''CREATE TABLE towns_with_coordinates
#     (town text,
#     north real,
#     east real)''')
#     for i in result.nodes:
#         # print(i.tags)
#         # print(str(i.lat) + str(i.lon) + i.tags['name'])
#         try:
#             cur.execute(
#                 "insert into towns_with_coordinates(town, north, east) "
#                 "values (\'{}\', {}, {})".format(i.tags['name'], str(i.lat), str(i.lon)))
#         except sqlite3.OperationalError:
#             print('sqlite3.operational error on {}, stacktrace folows:'.format(
#                 i.tags['name']))
#             print(traceback.format_exc())
#     cur.execute("CREATE INDEX towns ON towns_with_coordinates (town);")
#     con.commit()
#     con.close()

# if len(sys.argv) == 1:
#     get_database_of_lost_places_sqlitedb()
# elif len(sys.argv) == 2:
#     get_database_of_lost_places_pages(sys.argv[1])
# else:
#     print('0 arguments or 1 argument required - path, where to save database of lost places')
