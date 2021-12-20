# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_map_drawer.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(1059, 911)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(930, 10, 121, 23))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(930, 40, 121, 23))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(830, 10, 91, 20))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(830, 40, 91, 20))
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(970, 100, 80, 23))
        self.pushButton.setObjectName("pushButton")
        self.graphicsViewMapCanvas = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsViewMapCanvas.setGeometry(QtCore.QRect(830, 610, 221, 231))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsViewMapCanvas.sizePolicy().hasHeightForWidth())
        self.graphicsViewMapCanvas.setSizePolicy(sizePolicy)
        self.graphicsViewMapCanvas.setObjectName("graphicsViewMapCanvas")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 801, 841))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(1)
        self.gridLayout.setObjectName("gridLayout")
        self.graphicsView = QtWidgets.QGraphicsView(self.gridLayoutWidget)
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout.addWidget(self.graphicsView, 0, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(830, 70, 57, 15))
        self.label_3.setObjectName("label_3")
        self.lineEdit_town = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_town.setGeometry(QtCore.QRect(930, 70, 121, 21))
        self.lineEdit_town.setObjectName("lineEdit_town")
        self.pushButton_save_map = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_save_map.setGeometry(QtCore.QRect(970, 540, 80, 23))
        self.pushButton_save_map.setObjectName("pushButton_save_map")
        self.lineEdit_save_html = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_save_html.setGeometry(QtCore.QRect(940, 570, 113, 23))
        self.lineEdit_save_html.setObjectName("lineEdit_save_html")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1059, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Map drawer"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "latitude, longitude"))
        self.label.setText(_translate("MainWindow", "center"))
        self.label_2.setText(_translate("MainWindow", "radius"))
        self.pushButton.setText(_translate("MainWindow", "Draw map"))
        self.label_3.setText(_translate("MainWindow", "Town"))
        self.pushButton_save_map.setText(_translate("MainWindow", "Save map"))
        self.lineEdit_save_html.setPlaceholderText(_translate("MainWindow", "path to save map"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
