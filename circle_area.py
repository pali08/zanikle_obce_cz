import sqlite3

import staticmaps

from database_handling_queries import get_places_in_radius, DB_FILE


def create_area(center, radius):
    context = staticmaps.Context()
    context.set_tile_provider(staticmaps.tile_provider_OSM)
    center = [float(i.strip()) for i in center.split(',')]
    places = get_places_in_radius(center, radius, sqlite3.connect(DB_FILE))
    center_latln = staticmaps.create_latlng(center[0], center[1])
    context.add_object(
        staticmaps.Circle(center_latln, radius, fill_color=staticmaps.TRANSPARENT, color=staticmaps.RED, width=2))
    context.add_object(staticmaps.Marker(center_latln, size=5, color=staticmaps.BLACK))
    for place in places:
        place_latlng = staticmaps.create_latlng(place[-2], place[-1])
        context.add_object(staticmaps.Marker(place_latlng, size=5, color=staticmaps.RED))
    return context


def write_png(context, filepath):
    image = context.render_cairo(800, 600)
    image.write_to_png(filepath)


def get_image(center, radius, filepath=None):
    if filepath is None:
        print('File is not saved.')
        return
    context = create_area(center, radius)
    write_png(context, filepath)
