import io
import sys
import time

import folium
from PyQt6 import QtWidgets, QtWebEngineWidgets

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    m = folium.Map(
        location=[45.5236, -122.6750], tiles="Stamen Toner", zoom_start=13
    )

    data = io.BytesIO()
    print('asd')
    #print(data)
    print('asd')
    m.save(data, close_file=False)

    w = QtWebEngineWidgets.QWebEngineView()
    with open('map3.html', mode='w', encoding='utf-8') as f:
        f.write(data.getvalue().decode())
    time.sleep(10)
    # with open('map3.html', mode='w', encoding='utf-8') as g:
    with open('/home/pali/PycharmProjects/zanikle_obce_cz/map3.html', mode='r', encoding='utf-8') as g:
        html_from_file = g.read()
    # print(data.getvalue())
    w.setHtml(html_from_file)
    # w.setHtml(data.getvalue().decode())
    w.resize(640, 480)
    w.show()

    sys.exit(app.exec())