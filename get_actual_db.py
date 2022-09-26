import csv
import json
import os.path
import sqlite3
import traceback
from io import StringIO
from shutil import move
from time import sleep

import requests
import urllib3.exceptions
from bs4 import BeautifulSoup

from get_data_from_page import get_data_of_place

url = 'http://www.zanikleobce.cz/index.php?menu=93&sort=1&l=&str=1'
url_main = 'http://www.zanikleobce.cz/'

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
    url = 'http://www.zanikleobce.cz/index.php?menu=93&sort=5&l=&str=1'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    last_page_link = soup.find('table').find('table').find('tr').find('td').findNext('td').findNext('td') \
        .find('div').findAll('a', recursive=False)[-1]
    return int(last_page_link.text)


def insert_into_table(cursor, full_link, place_id):
    data_of_lost_place = get_data_of_place(full_link)
    cursor.execute(
        "insert into database_lost_places(link, id, name, category, municipality, district, "
        "end_reason, end_years,"
        "actual_state, north, east) "
        "values (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', {}, {})".format(
            full_link, place_id, data_of_lost_place['name'], data_of_lost_place['category'],
            data_of_lost_place['municipality'],
            data_of_lost_place['district'], data_of_lost_place['end_reason'],
            data_of_lost_place['end_years'],
            data_of_lost_place['actual_state'], data_of_lost_place['N'],
            data_of_lost_place['E']
        ))


def try_getting_data(func, cursor, full_link, place_id):
    try:
        func(cursor, full_link, place_id)
    except (urllib3.exceptions.NewConnectionError, urllib3.exceptions.MaxRetryError,
            urllib3.exceptions.ProtocolError, ConnectionResetError) as urllib3ConnectionException:
        sleep(30)
        try:
            func(cursor, full_link, place_id)
        except (urllib3.exceptions.NewConnectionError, urllib3.exceptions.MaxRetryError,
                urllib3.exceptions.ProtocolError, ConnectionResetError) as urllib3ConnectionException:
            sleep(30)
            try:
                func(cursor, full_link, place_id)
            except (urllib3.exceptions.NewConnectionError, urllib3.exceptions.MaxRetryError,
                    urllib3.exceptions.ProtocolError, ConnectionResetError) as urllib3ConnectionException:
                print(
                    f'Unable to get data for {full_link}, because following exception occured:'
                    f'{os.linesep}{urllib3ConnectionException}')


def load_program_data():
    with open('program_data.json', mode='r', encoding='utf-8') as f:
        data_loaded = json.load(f)
    return data_loaded


def edit_program_data(**kwargs):
    data = load_program_data()
    with open('program_data.json', mode='w') as out:
        for key, value in kwargs.items():
            if value is not None:
                data[key] = value
        json_object = json.dumps(data)
        out.write(json_object)


def iterate_over_pages_and_get_data(lowest_page, cursor, update_only=False, previous_highest_id=None):
    num_of_pages = get_number_of_pages()
    for i in range(lowest_page, num_of_pages + 1):
        url_lost_places = 'http://www.zanikleobce.cz/index.php?menu=93&sort=5&l=&str=' + str(i)
        response = requests.get(url_lost_places)
        soup = BeautifulSoup(response.text, 'html.parser')
        table_lost_places = soup.find('table').find('table').find('table')
        for tr in table_lost_places.findAll("tr")[2:]:
            full_link = url_main + tr.find('td').find('a')['href']
            place_id = int(full_link.split('=')[-1])
            if (update_only and place_id > previous_highest_id) or not update_only:
                try_getting_data(insert_into_table, cursor, full_link, place_id)
    edit_program_data(highest_page=num_of_pages, highest_id=place_id)


def get_table_of_lost_places():
    if not connection_is_ok():
        return
    backup_db()
    # num_of_pages = get_number_of_pages()
    con = sqlite3.connect(os.path.join('.', 'database.db'))
    cur = con.cursor()
    cur.execute('''CREATE TABLE database_lost_places 
    (link text primary key,
    id integer,
    name text, 
    category text,
    municipality text,
    district text, 
    end_reason text, 
    end_years text, 
    actual_state text, 
    north real, 
    east real)''')
    iterate_over_pages_and_get_data(1, cur)
    cur.execute("CREATE INDEX index_north ON database_lost_places (north);")
    cur.execute("CREATE INDEX index_east ON database_lost_places (east);")
    con.commit()
    con.close()
    print('Database update/creation was finished (probably) successfully.'
          'Old database is backed up as database.db_bck. If in doubt (e.g. too many unexpected exceptions occurred), '
          'please replace database.db with database.db_bck')


def update_table_of_lost_places():
    program_data = load_program_data()
    con = sqlite3.connect(os.path.join('.', 'database.db'))
    cur = con.cursor()
    # highest page from previous run is lowest page now for next run
    lowest_page = program_data['highest_page']
    iterate_over_pages_and_get_data(lowest_page, cur, update_only=True, previous_highest_id=program_data['highest_id'])


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
