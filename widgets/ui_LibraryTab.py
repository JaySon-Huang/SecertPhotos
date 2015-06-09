# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/ui_LibraryTab.ui'
#
# Created: Tue Jun  9 21:46:41 2015
#      by: PyQt5 UI code generator 5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Tab(object):
    def setupUi(self, Tab):
        Tab.setObjectName("Tab")
        Tab.resize(762, 523)
        self.verticalLayout = QtWidgets.QVBoxLayout(Tab)
        self.verticalLayout.setObjectName("verticalLayout")
        self.hLayout = QtWidgets.QHBoxLayout()
        self.hLayout.setObjectName("hLayout")
        self.btn_enterPassword = QtWidgets.QPushButton(Tab)
        self.btn_enterPassword.setObjectName("btn_enterPassword")
        self.hLayout.addWidget(self.btn_enterPassword)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.hLayout)
        self.scrollArea = QtWidgets.QScrollArea(Tab)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 736, 455))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)

        self.retranslateUi(Tab)
        QtCore.QMetaObject.connectSlotsByName(Tab)

    def retranslateUi(self, Tab):
        _translate = QtCore.QCoreApplication.translate
        Tab.setWindowTitle(_translate("Tab", "Form"))
        self.btn_enterPassword.setText(_translate("Tab", "Enter Password"))

