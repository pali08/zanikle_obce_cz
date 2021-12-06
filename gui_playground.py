import os
from pathlib import Path

from PyQt5.QtGui import QPixmap

from circle_area_webpage import show_html_map_with_markers
from gui_map_drawer import Ui_MainWindow

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox, QGraphicsPixmapItem, QGraphicsScene, \
    QFileDialog
from PyQt5.QtCore import QFile, pyqtSlot

# from ui_mainwindow import Ui_MainWindow
from circle_area import get_image


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.on_click)
        # self.ui.pushButtonSetPath.clicked.connect(self.on_click_set_path)
        self.show()

    def set_filename_open(self):
        return QFileDialog.getOpenFileName(self, "Open Image", str(Path.home()), "Image Files (*.png *.jpg *.bmp)")

    def set_filename_save(self):
        if 'PYCHARM_HOSTED' in os.environ:
            return QFileDialog.getSaveFileName(self, caption="Save Image", directory=str(Path.home()),
                                               filter="Image Files (*.png *.jpg *.bmp)",
                                               options=QFileDialog.DontUseNativeDialog)
        else:
            return QFileDialog.getSaveFileName(self, caption="Save Image", directory=str(Path.home()),
                                               filter="Image Files (*.png *.jpg *.bmp)")

    def draw_image(self, image_path):
        pix = QPixmap(image_path)
        item = QGraphicsPixmapItem(pix)
        scene = QGraphicsScene(self)
        scene.addItem(item)
        self.ui.graphicsViewMapCanvas.setScene(scene)

    @pyqtSlot()
    def on_click(self):
        textbox_value_center = self.ui.lineEdit.text()
        textbox_value_radius = float(self.ui.lineEdit_2.text())
        image_filepath_save = 'map.png'
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
        html_map_filepath = 'map.html'
        show_html_map_with_markers(textbox_value_center, textbox_value_radius, html_map_filepath)
        QMessageBox.question(self, 'File save', 'Map in html page format was saved to ' + html_map_filepath,
                             QMessageBox.Ok,
                             QMessageBox.Ok)

    # @pyqtSlot()
    # def on_click_set_path(self):
    #     QFileDialog.getSaveFileName()
    #     self.ui.lineEdit_save_image.setText(self.set_filename_open())


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
