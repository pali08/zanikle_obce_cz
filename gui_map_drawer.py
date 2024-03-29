# Form implementation generated from reading ui file 'gui_map_drawer.ui'
#
# Created by: PyQt6 UI code generator 6.3.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.WindowModality.NonModal)
        MainWindow.resize(1059, 911)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(100)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout.setVerticalSpacing(7)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.scrollArea_places_buttons = QtWidgets.QScrollArea(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea_places_buttons.sizePolicy().hasHeightForWidth())
        self.scrollArea_places_buttons.setSizePolicy(sizePolicy)
        self.scrollArea_places_buttons.setWidgetResizable(True)
        self.scrollArea_places_buttons.setObjectName("scrollArea_places_buttons")
        self.scrollAreaWidgetContents_places_buttons = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_places_buttons.setGeometry(QtCore.QRect(0, 0, 255, 831))
        self.scrollAreaWidgetContents_places_buttons.setObjectName("scrollAreaWidgetContents_places_buttons")
        self.scrollArea_places_buttons.setWidget(self.scrollAreaWidgetContents_places_buttons)
        self.horizontalLayout.addWidget(self.scrollArea_places_buttons)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 1, 1, 1)
        self.gridLayout_html_map = QtWidgets.QGridLayout()
        self.gridLayout_html_map.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMaximumSize)
        self.gridLayout_html_map.setSpacing(0)
        self.gridLayout_html_map.setObjectName("gridLayout_html_map")
        self.label_type = QtWidgets.QLabel(self.centralwidget)
        self.label_type.setObjectName("label_type")
        self.gridLayout_html_map.addWidget(self.label_type, 5, 2, 1, 1)
        self.pushButton_draw_map_radius_around_town = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_draw_map_radius_around_town.setObjectName("pushButton_draw_map_radius_around_town")
        self.gridLayout_html_map.addWidget(self.pushButton_draw_map_radius_around_town, 4, 5, 1, 1)
        self.comboBox_status = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_status.setObjectName("comboBox_status")
        self.gridLayout_html_map.addWidget(self.comboBox_status, 5, 1, 1, 1)
        self.pushButton_draw_map_by_coordinates = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_draw_map_by_coordinates.setObjectName("pushButton_draw_map_by_coordinates")
        self.gridLayout_html_map.addWidget(self.pushButton_draw_map_by_coordinates, 0, 5, 1, 1)
        self.pushButton_draw_map_by_town = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_draw_map_by_town.setObjectName("pushButton_draw_map_by_town")
        self.gridLayout_html_map.addWidget(self.pushButton_draw_map_by_town, 1, 5, 1, 1)
        self.pushButton_save_map_img = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_save_map_img.setObjectName("pushButton_save_map_img")
        self.gridLayout_html_map.addWidget(self.pushButton_save_map_img, 1, 7, 1, 1)
        self.lineEdit_radius = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_radius.setObjectName("lineEdit_radius")
        self.gridLayout_html_map.addWidget(self.lineEdit_radius, 0, 1, 1, 1)
        self.qWebEngineView_html_map = QtWebEngineWidgets.QWebEngineView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(8)
        sizePolicy.setHeightForWidth(self.qWebEngineView_html_map.sizePolicy().hasHeightForWidth())
        self.qWebEngineView_html_map.setSizePolicy(sizePolicy)
        self.qWebEngineView_html_map.setObjectName("qWebEngineView_html_map")
        self.gridLayout_html_map.addWidget(self.qWebEngineView_html_map, 7, 0, 2, 8)
        self.label_status = QtWidgets.QLabel(self.centralwidget)
        self.label_status.setObjectName("label_status")
        self.gridLayout_html_map.addWidget(self.label_status, 5, 0, 1, 1)
        self.lineEdit_town = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_town.setObjectName("lineEdit_town")
        self.gridLayout_html_map.addWidget(self.lineEdit_town, 4, 1, 1, 1)
        self.label_town = QtWidgets.QLabel(self.centralwidget)
        self.label_town.setObjectName("label_town")
        self.gridLayout_html_map.addWidget(self.label_town, 4, 0, 1, 1)
        self.label_radius = QtWidgets.QLabel(self.centralwidget)
        self.label_radius.setObjectName("label_radius")
        self.gridLayout_html_map.addWidget(self.label_radius, 0, 0, 1, 1)
        self.lineEdit_save_html = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_save_html.setObjectName("lineEdit_save_html")
        self.gridLayout_html_map.addWidget(self.lineEdit_save_html, 0, 6, 1, 1)
        self.pushButton_update_db = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_update_db.setObjectName("pushButton_update_db")
        self.gridLayout_html_map.addWidget(self.pushButton_update_db, 4, 7, 1, 1)
        self.comboBox_type = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_type.setObjectName("comboBox_type")
        self.gridLayout_html_map.addWidget(self.comboBox_type, 5, 3, 1, 1)
        self.lineEdit_center = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_center.setObjectName("lineEdit_center")
        self.gridLayout_html_map.addWidget(self.lineEdit_center, 1, 1, 1, 1)
        self.pushButton_save_map = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_save_map.setObjectName("pushButton_save_map")
        self.gridLayout_html_map.addWidget(self.pushButton_save_map, 0, 7, 1, 1)
        self.label_center = QtWidgets.QLabel(self.centralwidget)
        self.label_center.setObjectName("label_center")
        self.gridLayout_html_map.addWidget(self.label_center, 1, 0, 1, 1)
        self.label_draw_map = QtWidgets.QLabel(self.centralwidget)
        self.label_draw_map.setObjectName("label_draw_map")
        self.gridLayout_html_map.addWidget(self.label_draw_map, 0, 4, 1, 1)
        self.gridLayout_html_map.setColumnStretch(0, 1)
        self.gridLayout_html_map.setColumnStretch(1, 1)
        self.gridLayout_html_map.setColumnStretch(2, 1)
        self.gridLayout_html_map.setColumnStretch(3, 1)
        self.gridLayout_html_map.setColumnStretch(4, 2)
        self.gridLayout_html_map.setColumnStretch(5, 2)
        self.gridLayout_html_map.setColumnStretch(6, 2)
        self.gridLayout_html_map.setColumnStretch(7, 2)
        self.gridLayout.addLayout(self.gridLayout_html_map, 1, 0, 1, 1)
        self.gridLayout.setColumnStretch(0, 15)
        self.gridLayout.setColumnStretch(1, 5)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1059, 19))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.ToolBarArea.TopToolBarArea, self.toolBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Map drawer"))
        self.label_type.setText(_translate("MainWindow", "Type"))
        self.pushButton_draw_map_radius_around_town.setText(_translate("MainWindow", "radius around town"))
        self.pushButton_draw_map_by_coordinates.setText(_translate("MainWindow", "by coordinates"))
        self.pushButton_draw_map_by_town.setText(_translate("MainWindow", "by town (only)"))
        self.pushButton_save_map_img.setText(_translate("MainWindow", "Save map as png"))
        self.label_status.setText(_translate("MainWindow", "Status"))
        self.lineEdit_town.setPlaceholderText(_translate("MainWindow", "town, district"))
        self.label_town.setText(_translate("MainWindow", "Town"))
        self.label_radius.setText(_translate("MainWindow", "Radius"))
        self.lineEdit_save_html.setPlaceholderText(_translate("MainWindow", "path to save map"))
        self.pushButton_update_db.setText(_translate("MainWindow", "Update database"))
        self.lineEdit_center.setPlaceholderText(_translate("MainWindow", "latitude, longitude"))
        self.pushButton_save_map.setText(_translate("MainWindow", "Save map as html"))
        self.label_center.setText(_translate("MainWindow", "Center"))
        self.label_draw_map.setText(_translate("MainWindow", "Draw map"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
from PyQt6 import QtWebEngineWidgets
