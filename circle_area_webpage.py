import sqlite3

import folium
from folium.map import Popup
from IPython.display import HTML, display
from database_handling_queries import get_places_in_radius, DB_FILE, get_places_by_municipality


def add_places_to_map(map, filepath, places):
    for i in places:
        # this should be handled in query (not null), but just to be sure
        if i[-2] is not None and i[-1] is not None:
            folium.CircleMarker(location=tuple([i[-2], i[-1]]), popup=Popup(i[1], show=True)).add_to(map)
    map.save(filepath)
    # display(map)


def show_html_map_with_markers(center, radius, filepath):
    center_list = [float(i.strip()) for i in center.split(',')]
    places = get_places_in_radius(center_list, radius, sqlite3.connect(DB_FILE))
    m = folium.Map(location=center_list)
    folium.CircleMarker(location=tuple(center_list), popup=Popup('Picasso', show=True)).add_to(m)
    # print(places)
    add_places_to_map(m, filepath, places)


def show_html_map_with_markers_town(municipality, filepath):
    places = get_places_by_municipality(municipality, sqlite3.connect(DB_FILE))
    # we will add first places, otherwise initial map is un-zoomed
    m = folium.Map(location=(places[0][-2], places[0][-1]))
    add_places_to_map(m, filepath, places)

# show_html_map_with_markers('49.9,14.8', '20')
