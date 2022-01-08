import os
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


def get_places_in_radius(specified_point, radius, db_connection):
    specified_point_latitude = str(specified_point[0])
    specified_point_longitude = str(specified_point[1])
    db_connection.create_function('getdistance', 4, get_distance)
    cursor = db_connection.cursor()
    cursor.execute(
        'SELECT * FROM database_lost_places WHERE getdistance({}, {}, north, east) < {} and north is not null and '
        'east is not null'.format(
            str(specified_point_latitude), str(specified_point_longitude), str(radius)))
    rows = cursor.fetchall()
    db_connection.close()
    return rows


def get_places_by_municipality(municipality, db_connection):
    cursor = db_connection.cursor()
    cursor.execute('SELECT * FROM database_lost_places WHERE lower(municipality)=lower(\'{}\')'.format(municipality))
    rows = cursor.fetchall()
    db_connection.close()
    return rows
