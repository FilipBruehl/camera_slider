# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 720)
        MainWindow.setMinimumSize(QtCore.QSize(1280, 720))
        MainWindow.setMaximumSize(QtCore.QSize(1280, 720))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(14)
        MainWindow.setFont(font)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("background-color: #fff;")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(12)
        self.centralwidget.setFont(font)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1281, 691))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_left = QtWidgets.QVBoxLayout()
        self.verticalLayout_left.setObjectName("verticalLayout_left")
        self.horizontalLayout.addLayout(self.verticalLayout_left)
        self.verticalLayout_center = QtWidgets.QVBoxLayout()
        self.verticalLayout_center.setObjectName("verticalLayout_center")
        self.horizontalLayout.addLayout(self.verticalLayout_center)
        self.verticalLayout_right = QtWidgets.QVBoxLayout()
        self.verticalLayout_right.setObjectName("verticalLayout_right")
        self.groupBox_info = QtWidgets.QGroupBox(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_info.setFont(font)
        self.groupBox_info.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_info.setFlat(False)
        self.groupBox_info.setCheckable(False)
        self.groupBox_info.setObjectName("groupBox_info")
        self.groupBox_info_server = QtWidgets.QGroupBox(self.groupBox_info)
        self.groupBox_info_server.setGeometry(QtCore.QRect(10, 30, 400, 50))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_info_server.sizePolicy().hasHeightForWidth())
        self.groupBox_info_server.setSizePolicy(sizePolicy)
        self.groupBox_info_server.setMinimumSize(QtCore.QSize(400, 50))
        self.groupBox_info_server.setMaximumSize(QtCore.QSize(400, 50))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(10)
        self.groupBox_info_server.setFont(font)
        self.groupBox_info_server.setStyleSheet("border-color: #000;\n"
"border-radius: 5px;\n"
"border-style: solid;\n"
"border-width: 2px;\n"
"")
        self.groupBox_info_server.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_info_server.setObjectName("groupBox_info_server")
        self.label_info_server = QtWidgets.QLabel(self.groupBox_info_server)
        self.label_info_server.setGeometry(QtCore.QRect(15, 15, 185, 25))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(14)
        self.label_info_server.setFont(font)
        self.label_info_server.setStyleSheet("border: none;")
        self.label_info_server.setObjectName("label_info_server")
        self.label_info_server_ip = QtWidgets.QLabel(self.groupBox_info_server)
        self.label_info_server_ip.setGeometry(QtCore.QRect(210, 15, 185, 25))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(14)
        self.label_info_server_ip.setFont(font)
        self.label_info_server_ip.setStyleSheet("color: #DB2828;\n"
"border: none;")
        self.label_info_server_ip.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_info_server_ip.setObjectName("label_info_server_ip")
        self.groupBox_info_kamera = QtWidgets.QGroupBox(self.groupBox_info)
        self.groupBox_info_kamera.setGeometry(QtCore.QRect(10, 100, 400, 50))
        self.groupBox_info_kamera.setMinimumSize(QtCore.QSize(400, 50))
        self.groupBox_info_kamera.setMaximumSize(QtCore.QSize(400, 50))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(10)
        self.groupBox_info_kamera.setFont(font)
        self.groupBox_info_kamera.setStyleSheet("border-color: #000;\n"
"border-radius: 5px;\n"
"border-style: solid;\n"
"border-width: 2px;")
        self.groupBox_info_kamera.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_info_kamera.setObjectName("groupBox_info_kamera")
        self.horizontalLayoutWidget_4 = QtWidgets.QWidget(self.groupBox_info_kamera)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(10, 10, 381, 31))
        self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")
        self.horizontalLayout_info_kamera = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.horizontalLayout_info_kamera.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_info_kamera.setObjectName("horizontalLayout_info_kamera")
        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget_4)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("border: none;\n"
"background-color: transparent;")
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_info_kamera.addWidget(self.label_2)
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget_4)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setStyleSheet("background-color: transparent;\n"
"border: none;\n"
"color: #DB2828;")
        self.label.setObjectName("label")
        self.horizontalLayout_info_kamera.addWidget(self.label)
        self.groupBox_info_slider = QtWidgets.QGroupBox(self.groupBox_info)
        self.groupBox_info_slider.setGeometry(QtCore.QRect(10, 170, 400, 100))
        self.groupBox_info_slider.setMinimumSize(QtCore.QSize(400, 100))
        self.groupBox_info_slider.setMaximumSize(QtCore.QSize(400, 100))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(10)
        self.groupBox_info_slider.setFont(font)
        self.groupBox_info_slider.setStyleSheet("border-color: #000;\n"
"border-radius: 5px;\n"
"border-style: solid;\n"
"border-width: 2px;")
        self.groupBox_info_slider.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_info_slider.setObjectName("groupBox_info_slider")
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self.groupBox_info_slider)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(10, 10, 381, 81))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.horizontalLayout_info_slider = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_info_slider.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_info_slider.setObjectName("horizontalLayout_info_slider")
        self.verticalLayout_right.addWidget(self.groupBox_info)
        self.horizontalLayout.addLayout(self.verticalLayout_right)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 22))
        self.menubar.setMinimumSize(QtCore.QSize(1280, 22))
        self.menubar.setMaximumSize(QtCore.QSize(1280, 22))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(10)
        self.menubar.setFont(font)
        self.menubar.setObjectName("menubar")
        self.menuServer = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        self.menuServer.setFont(font)
        self.menuServer.setObjectName("menuServer")
        self.menuSchliessen = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        self.menuSchliessen.setFont(font)
        self.menuSchliessen.setObjectName("menuSchliessen")
        self.menuUeber = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        self.menuUeber.setFont(font)
        self.menuUeber.setObjectName("menuUeber")
        MainWindow.setMenuBar(self.menubar)
        self.actionConnect = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        self.actionConnect.setFont(font)
        self.actionConnect.setObjectName("actionConnect")
        self.actionDisconnect = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        self.actionDisconnect.setFont(font)
        self.actionDisconnect.setObjectName("actionDisconnect")
        self.actionConnectCamera = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        self.actionConnectCamera.setFont(font)
        self.actionConnectCamera.setObjectName("actionConnectCamera")
        self.actionExportieren = QtWidgets.QAction(MainWindow)
        self.actionExportieren.setObjectName("actionExportieren")
        self.actionImportieren = QtWidgets.QAction(MainWindow)
        self.actionImportieren.setObjectName("actionImportieren")
        self.menuServer.addAction(self.actionConnect)
        self.menuServer.addAction(self.actionDisconnect)
        self.menuServer.addSeparator()
        self.menuServer.addAction(self.actionConnectCamera)
        self.menubar.addAction(self.menuServer.menuAction())
        self.menubar.addAction(self.menuUeber.menuAction())
        self.menubar.addAction(self.menuSchliessen.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Camera Slider"))
        self.groupBox_info.setTitle(_translate("MainWindow", "Informationen"))
        self.groupBox_info_server.setTitle(_translate("MainWindow", "Server"))
        self.label_info_server.setText(_translate("MainWindow", "Verbunden mit:"))
        self.label_info_server_ip.setText(_translate("MainWindow", "Nicht verbunden"))
        self.groupBox_info_kamera.setTitle(_translate("MainWindow", "Kamera"))
        self.label_2.setText(_translate("MainWindow", "Verbunden mit:"))
        self.label.setText(_translate("MainWindow", "Nicht verbunden"))
        self.groupBox_info_slider.setTitle(_translate("MainWindow", "Slider"))
        self.menuServer.setTitle(_translate("MainWindow", "Server"))
        self.menuSchliessen.setTitle(_translate("MainWindow", "Schließen"))
        self.menuUeber.setTitle(_translate("MainWindow", "Über"))
        self.actionConnect.setText(_translate("MainWindow", "Verbinden"))
        self.actionDisconnect.setText(_translate("MainWindow", "Verbindung trennen"))
        self.actionConnectCamera.setText(_translate("MainWindow", "Kamera verbinden"))
        self.actionExportieren.setText(_translate("MainWindow", "Exportieren"))
        self.actionImportieren.setText(_translate("MainWindow", "Importieren"))
