# import os
# import sys
# from PyQt5.Qt import *
# from PyQt5.QtWebEngineWidgets import *
# from PyQt5.QtWidgets import QApplication
#
# app = QApplication(sys.argv)
#
# web = QWebEngineView()
#
# # web.load(QUrl.fromLocalFile(app.applicationDirPath() + "./test_local_webpage.html"))
# file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "map.html"))
# web.load(QUrl.fromLocalFile(file_path))
#
# web.show()
#
# sys.exit(app.exec_())

import sys

from PyQt5.QtWidgets import QApplication, QGridLayout, QMainWindow, QTextEdit, QWidget
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView

url = "https://google.com"

app = QApplication(sys.argv)

w = QMainWindow()

browser = QWebEngineView()
browser.load(QUrl(url))

central_widget = QWidget()
w.setCentralWidget(central_widget)

lay = QGridLayout(central_widget)
lay.addWidget(browser, 0, 0, 2, 1)
lay.addWidget(QTextEdit(), 0, 1)
lay.addWidget(QTextEdit(), 1, 1)

# lay.setColumnStretch(0, 1)
# lay.setColumnStretch(1, 1)
#
# lay.setRowStretch(0, 1)
# lay.setRowStretch(1, 1)

w.show()

sys.exit(app.exec_())