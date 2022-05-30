from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtWebEngineWidgets import *
import sys

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow,self).__init__(*args, **kwargs)
        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)
        with open('/home/pali/PycharmProjects/zanikle_obce_cz/map.html', mode='r', encoding='utf-8') as f:
            text = f.read()
        self.browser.setHtml(text)
        # self.browser.setUrl(QUrl("https://www.google.com"))
        # self.browser.setUrl(QUrl("https://www.openstreetmap.org/#map=7/49.817/15.478"))
        # self.browser.setHtml("<html><body><h1>Hello World... Hello World</h1></body></html>")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()  # moved show outside main widget
    sys.exit(app.exec())   #  use app.exec instead of app.exec_
