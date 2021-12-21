import os
from pathlib import Path
from shutil import copyfile

from PyQt5.QtGui import QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView

from circle_area_webpage import show_html_map_with_markers
from gui_map_drawer import Ui_MainWindow

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox, QGraphicsPixmapItem, QGraphicsScene, \
    QFileDialog, QTextEdit, QWidget, QGridLayout
from PyQt5.QtCore import QFile, pyqtSlot, QUrl

# from ui_mainwindow import Ui_MainWindow
from circle_area import get_image


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.gridLayout_html_map.setColumnStretch(0, 1)
        self.ui.gridLayout_html_map.setRowStretch(0, 1)
        self.ui.pushButton.clicked.connect(self.on_click_draw)
        self.ui.pushButton_save_map.clicked.connect(self.on_click_save_map)
        # self.ui.pushButtonSetPath.clicked.connect(self.on_click_set_path)
        self.show()

    def set_filename_open(self):
        return QFileDialog.getOpenFileName(self, "Open Image", str(Path.home()), "Image Files (*.png *.jpg *.bmp)")

    def set_filename_save(self):
        if 'PYCHARM_HOSTED' in os.environ:
            return QFileDialog.getSaveFileName(self, caption="Save Image", directory=str(Path.home()),
                                               filter="Html Files (*.html *.htm)",
                                               options=QFileDialog.DontUseNativeDialog)
        else:
            return QFileDialog.getSaveFileName(self, caption="Save Image", directory=str(Path.home()),
                                               filter="Html Files (*.html *.htm)")

    def draw_image(self, image_path):
        pix = QPixmap(image_path)
        item = QGraphicsPixmapItem(pix)
        scene = QGraphicsScene(self)
        scene.addItem(item)
        self.ui.graphicsView_png_map.setScene(scene)

    def show_html_map_in_grid(self):
        browser = QWebEngineView(self)
        url = 'https://google.com'
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'temporary_files', "map.html"))
        print(os.path.dirname(__file__))
        browser.load(QUrl.fromLocalFile(file_path))
        # self.ui.graphicsView_html_map.load(QUrl('map.html'))
        self.ui.gridLayout_html_map.addWidget(browser, 0, 0, 1, 1)

    @pyqtSlot()
    def on_click_draw(self):
        try:
            textbox_value_center = self.ui.lineEdit_center.text()
            textbox_value_radius = float(self.ui.lineEdit_radius.text())
            image_filepath_save = os.path.join('temporary_files', 'map.png')
            # image_filepath_save = self.ui.lineEdit_save_image.text()
            # while not os.path.exists(os.path.dirname(image_filepath_save)) or os.path.exists(
            #         image_filepath_save):
            #     QMessageBox.question(self, 'Problem saving file',
            #                          'Path not exists or file already exists. Pick another path', QMessageBox.Ok,
            #                          QMessageBox.Ok)
            #     image_filepath_save = self.set_filename_save()[0]
            #     print(image_filepath_save)
            #     self.ui.lineEdit_save_image.setText(image_filepath_save)
            get_image(textbox_value_center, textbox_value_radius,
                      filepath=image_filepath_save)
            self.draw_image(image_filepath_save)
            # get_image(49.4750, 15.8611, 49.5005, 15.9178)
            html_map_filepath = os.path.join('temporary_files', 'map.html')
            show_html_map_with_markers(textbox_value_center, textbox_value_radius, html_map_filepath)
            self.show_html_map_in_grid()
            QMessageBox.question(self, 'File save', 'Map in html page format was saved to ' + html_map_filepath,
                                 QMessageBox.Ok,
                                 QMessageBox.Ok)
        except ValueError:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText(
                "Input format of center or randius is incorrect. Set center as two numbers splitted by comma and "
                "radius in kilometers as one number")
            msgBox.setWindowTitle("Warning: Incorrect format of input")
            msgBox.setStandardButtons(QMessageBox.Close)
            # msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Close)
            msgBox.exec()
            # msgBox.buttonClicked.connect(msgButtonClick)

            # QMessageBox.Information(title='Warning', text='Unable to get center or radius. Check if format is correct')

    # @pyqtSlot()
    # def on_click_set_path(self):
    #     QFileDialog.getSaveFileName()
    #     self.ui.lineEdit_save_image.setText(self.set_filename_open())

    @pyqtSlot()
    def on_click_save_map(self):
        image_filepath_save = self.ui.lineEdit_save_html.text()
        while not os.path.exists(os.path.dirname(image_filepath_save)) or os.path.exists(image_filepath_save):
            QMessageBox.question(self, 'Problem saving file',
                                 'Directory not exists or file already exists. Pick another path', QMessageBox.Ok,
                                 QMessageBox.Ok)
            image_filepath_save = self.set_filename_save()[0]
            self.ui.lineEdit_save_html.setText(image_filepath_save)
        try:
            copyfile(os.path.join('temporary_files', 'map.html'), image_filepath_save)
        except PermissionError:
            QMessageBox.warning(self, 'Permission problem', 'Permission problem - pick another path')


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
