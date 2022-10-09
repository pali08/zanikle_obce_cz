import os
import sys
import time
from pathlib import Path
from shutil import copyfile
from time import sleep

import folium
from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSlot, QUrl, QRunnable, QThreadPool
from PyQt6.QtGui import QFontMetrics, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QGroupBox, QPushButton, QLabel, \
    QVBoxLayout, QTextBrowser, QTableView
from PyQt6.QtWidgets import QCompleter
from folium import Popup
from pyqt6_plugins.examplebuttonplugin import QtGui

from circle_area_webpage import get_html_map_with_markers, get_html_map_with_markers_town, \
    get_html_map_with_markers_town_and_radius, add_places_to_map
from database_handling_queries import get_all_towns
from get_actual_db import get_table_of_lost_places, get_center_town_coordinates, update_table_of_lost_places
from gui_map_drawer import Ui_MainWindow


def input_number_correct(count_of_numbers, input):
    if len(input.split(',')) == count_of_numbers:
        for i in input.split(','):
            try:
                float(i)
            except ValueError:
                return False
        return True
    else:
        return False


class DbUpdaterComplete(QRunnable):
    """
    Database updater to run update in individual thread
    """

    def __init__(self, label):
        super(DbUpdaterComplete, self).__init__()
        self.label = label

    @pyqtSlot()
    def run(self):
        """
        Update database in thread
        """
        self.label.setText("Complete update started. DO NOT CLOSE PROGRAM")
        get_table_of_lost_places()
        get_center_town_coordinates()
        self.label.setText("Complete update finished.")


class DbUpdaterNewlyAdded(QRunnable):
    """
    Database updater to run update in individual thread
    """

    def __init__(self, label):
        super(DbUpdaterNewlyAdded, self).__init__()
        self.label = label

    @pyqtSlot()
    def run(self):
        """
        Update database in thread
        """
        self.label.setText("Update of newly added places started. DO NOT CLOSE PROGRAM")
        update_table_of_lost_places()
        get_center_town_coordinates()
        self.label.setText("Update of newly added places finished")


class MainWindow(QMainWindow):
    def __init__(self):
        towns = get_all_towns()
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.html_map_filepath = os.path.join('temporary_files', 'map.html')
        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        self.ui.gridLayout_html_map.setColumnStretch(0, 1)
        self.ui.gridLayout_html_map.setRowStretch(0, 1)
        self.ui.pushButton_draw_map_by_coordinates.clicked.connect(self.on_click_draw)
        self.ui.pushButton_save_map.clicked.connect(self.on_click_save_map_html)
        self.ui.pushButton_save_map_img.clicked.connect(self.on_click_save_map_img)
        self.ui.pushButton_draw_map_by_town.clicked.connect(self.on_click_draw_by_town)
        self.ui.pushButton_update_db.clicked.connect(self.on_click_update_db)
        self.ui.pushButton_draw_map_radius_around_town.clicked.connect(self.on_click_draw_by_radius_around_town)
        self.towns = towns
        self.completer = QCompleter(self.towns)
        self.completer.setCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)
        self.ui.lineEdit_town.setCompleter(self.completer)
        self.layout = QVBoxLayout(self.ui.scrollAreaWidgetContents_places_buttons)
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
        # keeping this here - possible problems in future (if I remember correctly, this caused problem in pyqt5)
        # if 'PYCHARM_HOSTED' in os.environ:
        #    return dialog.getSaveFileName(self, caption="Save map as {}".format(save_format),
        #                                  directory=str(Path.home()),
        #                                  filter=save_filter,
        #                                  options=QFileDialog.DontUseNativeDialog)
        # else:
        return dialog.getSaveFileName(self, caption="Save map as {}".format(save_format),
                                      directory=str(Path.home()),
                                      filter=save_filter)

    def show_html_map_in_grid(self):
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'temporary_files', "map.html"))
        with open(file_path, mode='r', encoding='utf-8') as f:
            html_map = f.read()
        self.ui.qWebEngineView_html_map.setHtml(html_map)
        self.ui.gridLayout_html_map.addWidget(self.ui.qWebEngineView_html_map, 6, 0, 1, 6)

    @pyqtSlot()
    def get_clicked_town_map(self, places, index_of_place):
        m = folium.Map(location=(places[index_of_place][-2], places[index_of_place][-1]))
        folium.CircleMarker(location=(places[index_of_place][-2], places[index_of_place][-1]),
                            popup=Popup('Picasso', show=True)).add_to(m)
        filepath = os.path.join('temporary_files', 'map.html')
        add_places_to_map(m, filepath, [places[index_of_place]])

    def print_places_into_scroll_area(self, places):
        def load_and_show(places_, i_):
            self.get_clicked_town_map(places_, i_)
            self.show_html_map_in_grid()

        for i in range(0, len(places)):
            button_town = QPushButton(places[i][1], self.ui.scrollAreaWidgetContents_places_buttons)
            text_area = QTextBrowser()
            text_area.anchorClicked.connect(QtGui.QDesktopServices.openUrl)
            text_area.setOpenExternalLinks(True)
            text_area.setOpenLinks(True)
            text_area.append('<a href="{}">{}</a>'.format(places[i][0], places[i][1]))
            for j in range(2, len(places[i])):
                text_area.append(str(places[i][j]))
            # this with lambda function is needed to add multiple buttons with different labels
            button_town.clicked.connect(lambda ch, i_lambda=i: load_and_show(places, i_lambda))
            font_metrics_height = text_area.fontMetrics().height()
            text_area.setMinimumHeight(font_metrics_height * (len(places[i]) + 1))
            text_area.setMaximumHeight(font_metrics_height * (len(places[i]) + 1))
            self.layout.addWidget(text_area)
            self.layout.addWidget(button_town)

    def on_click_save_map(self, save_format):
        image_filepath_save = self.ui.lineEdit_save_html.text()
        if not os.path.exists(os.path.dirname(image_filepath_save)) or os.path.exists(image_filepath_save):
            QMessageBox.question(self, 'Problem saving file',
                                 'Directory not exists or file already exists. Pick another path',
                                 QMessageBox.StandardButton.Ok,
                                 QMessageBox.StandardButton.Ok)
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

    def places_empty(self, places):
        if not places:
            QMessageBox.warning(self, 'Nothing found.', 'For given input no abandoned place was found',
                                QMessageBox.StandardButton.Close,
                                QMessageBox.StandardButton.Close)
            return True

    def remove_places_from_layout(self):
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)

    @pyqtSlot()
    def on_click_draw(self):
        self.remove_places_from_layout()
        if not (input_number_correct(2, self.ui.lineEdit_center.text())
                and input_number_correct(1, self.ui.lineEdit_radius.text())):
            QMessageBox.warning(self, 'Incorrect input', 'Incorrect input for radius or center',
                                QMessageBox.StandardButton.Close,
                                QMessageBox.StandardButton.Close)
            return
        textbox_value_center = self.ui.lineEdit_center.text()
        textbox_value_radius = float(self.ui.lineEdit_radius.text())
        html_map_filepath = os.path.join('temporary_files', 'map.html')
        places = get_html_map_with_markers(textbox_value_center, textbox_value_radius, html_map_filepath)
        if self.places_empty(places):
            return
        self.print_places_into_scroll_area(places)
        self.show_html_map_in_grid()

    @pyqtSlot()
    def on_click_draw_by_town(self):
        self.remove_places_from_layout()
        places = get_html_map_with_markers_town(self.ui.lineEdit_town.text(), self.html_map_filepath)
        if self.places_empty(places):
            return
        self.print_places_into_scroll_area(places)
        self.show_html_map_in_grid()

    @pyqtSlot()
    def on_click_draw_by_radius_around_town(self):
        self.remove_places_from_layout()
        if not input_number_correct(1, self.ui.lineEdit_radius.text()):
            QMessageBox.warning(self, 'Incorrect input', 'Incorrect input for radius', QMessageBox.StandardButton.Close,
                                QMessageBox.StandardButton.Close)
            return
        places = get_html_map_with_markers_town_and_radius(self.ui.lineEdit_town.text(), self.ui.lineEdit_radius.text(),
                                                           self.html_map_filepath)
        if self.places_empty(places):
            return
        self.print_places_into_scroll_area(places)
        self.show_html_map_in_grid()

    def run_complete_update_in_pool(self):
        worker = DbUpdaterComplete(self.ui.label)
        self.threadpool.start(worker)

    def run_update_newly_added_in_pool(self):
        worker = DbUpdaterNewlyAdded(self.ui.label)
        self.threadpool.start(worker)

    def on_click_update_db(self):
        box = QMessageBox()
        box.setWindowTitle('Database update')
        box.setText('Update database\n- Complete update: remove database and get new. It might take few hours, '
                    'but if previously added places changed after adding, changes will be updated\n- Newly added: get '
                    'only newly added places. Faster, but in case place was added before last database update and '
                    'changed after it, those changes will not be transfered to database.')
        box.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel)
        button_complete_update = box.button(QMessageBox.StandardButton.Yes)
        button_complete_update.setText('Complete update')
        button_complete_update.setIcon(QIcon(None))
        button_newly_added = box.button(QMessageBox.StandardButton.No)
        button_newly_added.setText('Newly added')
        button_newly_added.setIcon(QIcon(None))
        box.exec()

        if box.clickedButton() == button_complete_update:
            self.run_complete_update_in_pool()
        if box.clickedButton() == button_newly_added:
            self.run_update_newly_added_in_pool()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
