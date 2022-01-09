import os
import sys
from pathlib import Path
from shutil import copyfile

from PyQt5.QtCore import pyqtSlot, QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog

from circle_area_webpage import show_html_map_with_markers, show_html_map_with_markers_town
from gui_map_drawer import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.gridLayout_html_map.setColumnStretch(0, 1)
        self.ui.gridLayout_html_map.setRowStretch(0, 1)
        self.ui.pushButton_draw_map_by_coordinates.clicked.connect(self.on_click_draw)
        self.ui.pushButton_save_map.clicked.connect(self.on_click_save_map_html)
        self.ui.pushButton_save_map_img.clicked.connect(self.on_click_save_map_img)
        self.ui.pushButton_draw_map_by_town.clicked.connect(self.on_click_draw_by_town)
        self.show()

    def set_filename_open(self):
        return QFileDialog.getOpenFileName(self, "Open Image", str(Path.home()), "Image Files (*.png *.jpg *.bmp)")

    def set_filename_save(self, save_format):
        dialog = QFileDialog()
        if save_format == 'html':
            dialog.setDefaultSuffix('html')
            save_filter = 'Html Files (*.html *.htm)'
        elif save_format == 'png':
            dialog.setDefaultSuffix('png')
            save_filter = 'Image Files (*.png *.jpg *.bmp)'
        if 'PYCHARM_HOSTED' in os.environ:
            return dialog.getSaveFileName(self, caption="Save map as {}".format(save_format),
                                          directory=str(Path.home()),
                                          filter=save_filter,
                                          options=QFileDialog.DontUseNativeDialog)
        else:
            return dialog.getSaveFileName(self, caption="Save map as {}".format(save_format),
                                          directory=str(Path.home()),
                                          filter=save_filter)

    def show_html_map_in_grid(self):
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'temporary_files', "map.html"))
        self.ui.qWebEngineView_html_map.load(QUrl.fromLocalFile(file_path))
        self.ui.gridLayout_html_map.addWidget(self.ui.qWebEngineView_html_map, 6, 0, 1, 6)

    def print_places_into_text_browser(self, places):
        for place in places:
            for item in place:
                self.ui.textBrowser_places_info.append(str(item))
            self.ui.textBrowser_places_info.append(20*'-')


    @pyqtSlot()
    def on_click_draw(self):
        try:
            textbox_value_center = self.ui.lineEdit_center.text()
            textbox_value_radius = float(self.ui.lineEdit_radius.text())
            html_map_filepath = os.path.join('temporary_files', 'map.html')
            places = show_html_map_with_markers(textbox_value_center, textbox_value_radius, html_map_filepath)
            self.print_places_into_text_browser(places)
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
            msgBox.exec()

    def on_click_save_map(self, save_format):
        image_filepath_save = self.ui.lineEdit_save_html.text()
        if not os.path.exists(os.path.dirname(image_filepath_save)) or os.path.exists(image_filepath_save):
            QMessageBox.question(self, 'Problem saving file',
                                 'Directory not exists or file already exists. Pick another path', QMessageBox.Ok,
                                 QMessageBox.Ok)
            image_filepath_save = self.set_filename_save(save_format)[0]
            self.ui.lineEdit_save_html.setText(image_filepath_save)
        try:
            if save_format == 'png':
                self.ui.qWebEngineView_html_map.grab().save(image_filepath_save)
            elif save_format == 'html':
                copyfile(os.path.join('temporary_files', 'map.html'), image_filepath_save)
            else:
                print('on_click_save_map_function - format must be img or html')
                return
        except PermissionError:
            QMessageBox.warning(self, 'Permission problem', 'Permission problem - pick another path')
        except FileNotFoundError:
            pass

    @pyqtSlot()
    def on_click_save_map_img(self):
        self.on_click_save_map('png')

    @pyqtSlot()
    def on_click_save_map_html(self):
        self.on_click_save_map('html')


    @pyqtSlot()
    def on_click_draw_by_town(self):
        html_map_filepath = os.path.join('temporary_files', 'map.html')
        places = show_html_map_with_markers_town(self.ui.lineEdit_town.text(), html_map_filepath)
        self.print_places_into_text_browser(places)
        self.show_html_map_in_grid()
        QMessageBox.question(self, 'File save', 'Map in html page format was saved to ' + html_map_filepath,
                             QMessageBox.Ok,
                             QMessageBox.Ok)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
