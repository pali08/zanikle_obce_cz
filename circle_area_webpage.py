import sqlite3

import folium
from folium.map import Popup
from IPython.display import HTML, display
from database_handling_queries import get_places_in_radius, DB_FILE


def show_html_map_with_markers(center, radius, filepath):
    center_list = [float(i.strip()) for i in center.split(',')]
    places = get_places_in_radius(center_list, radius, sqlite3.connect(DB_FILE))
    m = folium.Map(location=center_list)
    folium.CircleMarker(location=tuple(center_list), popup=Popup('Picasso', show=True)).add_to(m)
    print(places)
    for i in places:
        # this should be handled in query (not null), but just to be sure
        if i[-2] is not None and i[-1] is not None:
            folium.CircleMarker(location=tuple([i[-2], i[-1]]), popup=Popup(i[1], show=True)).add_to(m)
    m.save(filepath)
    # display(m)


# show_html_map_with_markers('49.9,14.8', '20')
