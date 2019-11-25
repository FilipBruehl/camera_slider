# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'connect_camera.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(450, 400)
        Dialog.setMinimumSize(QtCore.QSize(450, 400))
        Dialog.setMaximumSize(QtCore.QSize(450, 400))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(18)
        Dialog.setFont(font)
        Dialog.setStyleSheet("background-color: white;")
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 452, 401))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.gridLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_heading = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_heading.setMinimumSize(QtCore.QSize(450, 50))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_heading.setFont(font)
        self.label_heading.setObjectName("label_heading")
        self.verticalLayout.addWidget(self.label_heading, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.listView_cameras = QtWidgets.QListView(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(12)
        self.listView_cameras.setFont(font)
        self.listView_cameras.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked|QtWidgets.QAbstractItemView.EditKeyPressed|QtWidgets.QAbstractItemView.SelectedClicked)
        self.listView_cameras.setItemAlignment(QtCore.Qt.AlignLeading)
        self.listView_cameras.setObjectName("listView_cameras")
        self.verticalLayout.addWidget(self.listView_cameras)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 10, -1, 10)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_select = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_select.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_select.sizePolicy().hasHeightForWidth())
        self.pushButton_select.setSizePolicy(sizePolicy)
        self.pushButton_select.setMinimumSize(QtCore.QSize(150, 30))
        self.pushButton_select.setMaximumSize(QtCore.QSize(150, 30))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(18)
        self.pushButton_select.setFont(font)
        self.pushButton_select.setStyleSheet("border-radius: 5px;\n"
"border-width: 2px;\n"
"border-color: rgb(0, 0, 0);\n"
"border-style: solid;")
        self.pushButton_select.setObjectName("pushButton_select")
        self.horizontalLayout.addWidget(self.pushButton_select, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Kamera verbinden"))
        self.label_heading.setText(_translate("Dialog", "Mit Kamera verbinden"))
        self.pushButton_select.setText(_translate("Dialog", "Auswählen"))
