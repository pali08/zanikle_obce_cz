import sqlite3

import geopy.distance

DB_FILE = 'database.db'


def get_db_cursor(db_file):
    con = sqlite3.connect(db_file)
    return con.cursor()


def get_distance(latitude_specified_point, longitude_specified_point, latitude_place, longitude_place):
    return geopy.distance.distance([latitude_specified_point,
                                    longitude_specified_point],
                                   [latitude_place,
                                    longitude_place]).km


def filter_by_status_and_category(status, category, rows):
    if status != '':
        rows = [i for i in rows if i[7] == status]
    if category != '':
        rows = [i for i in rows if i[2] == category]
    return rows


def get_places_in_radius(specified_point, radius, db_connection, close_connection=True, status='', category=''):
    specified_point_latitude = str(specified_point[0])
    specified_point_longitude = str(specified_point[1])
    db_connection.create_function('getdistance', 4, get_distance)
    cursor = db_connection.cursor()
    cursor.execute(
        'SELECT link,name,category,municipality,district,end_reason,end_years,actual_state,north,east '
        'FROM database_lost_places WHERE getdistance({}, {}, north, east) < {} and north is not null and '
        'east is not null'.format(
            str(specified_point_latitude), str(specified_point_longitude), str(radius)))
    rows = cursor.fetchall()
    if close_connection:
        db_connection.close()
    return filter_by_status_and_category(status, category, rows)


def get_municipality_and_district(municipality):
    town, district = municipality.split(',')
    town = town.strip()
    district = district.strip()
    return town, district


def get_places_by_municipality(municipality, db_connection, status='', category=''):
    cursor = db_connection.cursor()
    if ',' in municipality:
        print('this branch is executed')
        town, district = get_municipality_and_district(municipality)
        cursor.execute(
            'SELECT link,name,category,municipality,district,end_reason,end_years,actual_state,north,east '
            'FROM database_lost_places WHERE lower(municipality)=lower(\'{}\') and lower(district) = lower('
            '\'{}\')'.format(
                town, district))
    else:
        cursor.execute(
            'SELECT link,name,category,municipality,district,end_reason,end_years,actual_state,north,east '
            'FROM database_lost_places WHERE lower(municipality)=lower(\'{}\')'.format(
                municipality))
    rows = cursor.fetchall()
    db_connection.close()
    return filter_by_status_and_category(status, category, rows)


def get_places_in_radius_around_municipality(municipality, radius, db_connection, status='', category=''):
    cursor = db_connection.cursor()
    if ',' in municipality:
        town, district = get_municipality_and_district(municipality)
        cursor.execute(
            'SELECT NORTH,EAST FROM towns_with_coordinates WHERE lower(town)=lower(\'{}\') AND lower(district)=lower('
            '\'{}\')'.format(
                town, district))
    else:
        cursor.execute(
            'SELECT NORTH,EAST FROM towns_with_coordinates WHERE lower(town)=lower(\'{}\')'.format(
                municipality))
    municipality_coordinates = cursor.fetchall()
    result = []
    # previus execution, should have only one pair (one city and district, but to be sure, that program does not crash,
    # if more places are there)
    for coordinate_pair in municipality_coordinates:
        result += get_places_in_radius(coordinate_pair, radius, db_connection, close_connection=False)
    db_connection.close()
    return filter_by_status_and_category(status, category, result)


def get_all_towns():
    db_connection = sqlite3.connect(DB_FILE)
    cursor = db_connection.cursor()
    cursor.execute('SELECT municipality FROM database_lost_places UNION SELECT town FROM towns_with_coordinates')
    towns = cursor.fetchall()
    db_connection.close()
    return [i[0] for i in towns]


def get_all_distinct(column_name):
    db_connection = sqlite3.connect(DB_FILE)
    cursor = db_connection.cursor()
    cursor.execute(
        f'SELECT DISTINCT {column_name} FROM database_lost_places')
    rows = cursor.fetchall()
    db_connection.close()
    return [i[0] for i in rows]


def get_all_statuses():
    return get_all_distinct('actual_state')


def get_all_categories():
    return get_all_distinct('category')
