import staticmaps


def create_area(*coords):
    context = staticmaps.Context()
    context.set_tile_provider(staticmaps.tile_provider_OSM)
    rectangle = [(coords[0], coords[1]), (coords[2], coords[1]), (coords[2], coords[3]), (coords[0], coords[3]),
                 (coords[0], coords[1])]

    context.add_object(
        staticmaps.Area(
            [staticmaps.create_latlng(lat, lng) for lat, lng in rectangle],
            fill_color=staticmaps.parse_color("#FFFFFF00"),
            width=2,
            color=staticmaps.BLUE,
        )
    )
    print(context)
    return context


def write_png(context, filepath):
    image = context.render_cairo(800, 600)
    image.write_to_png(filepath)


def write_svg(context, filepath):
    svg_image = context.render_svg(800, 600)
    with open(filepath, "w", encoding="utf-8") as f:
        svg_image.write(f, pretty=True)


def get_image(*coords, filepath=None, png_or_svg='png'):
    if filepath is None:
        print('File is not saved.')
        return
    context = create_area(*coords)
    if png_or_svg == 'png':
        write_png(context, filepath)
    elif png_or_svg == 'svg':
        write_svg(context, filepath)
