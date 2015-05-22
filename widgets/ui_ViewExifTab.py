# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/ui_ViewExifTab.ui'
#
# Created: Tue May 19 22:41:00 2015
#      by: PyQt5 UI code generator 5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Tab(object):
    def setupUi(self, Tab):
        Tab.setObjectName("Tab")
        Tab.resize(800, 600)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(Tab)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.vLayout = QtWidgets.QVBoxLayout()
        self.vLayout.setObjectName("vLayout")
        self.hLayout = QtWidgets.QHBoxLayout()
        self.hLayout.setObjectName("hLayout")
        self.btn_loadImage = QtWidgets.QPushButton(Tab)
        self.btn_loadImage.setObjectName("btn_loadImage")
        self.hLayout.addWidget(self.btn_loadImage)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hLayout.addItem(spacerItem)
        self.vLayout.addLayout(self.hLayout)
        self.line = QtWidgets.QFrame(Tab)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.vLayout.addWidget(self.line)
        self.lb_image = ImageLabel(Tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb_image.sizePolicy().hasHeightForWidth())
        self.lb_image.setSizePolicy(sizePolicy)
        self.lb_image.setMinimumSize(QtCore.QSize(400, 400))
        self.lb_image.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_image.setObjectName("lb_image")
        self.vLayout.addWidget(self.lb_image)
        self.lb_filename = QtWidgets.QLabel(Tab)
        self.lb_filename.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_filename.setObjectName("lb_filename")
        self.vLayout.addWidget(self.lb_filename)
        self.horizontalLayout_2.addLayout(self.vLayout)
        self.tv_exifTable = QtWidgets.QTableWidget(Tab)
        self.tv_exifTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tv_exifTable.setObjectName("tv_exifTable")
        self.tv_exifTable.setColumnCount(2)
        self.tv_exifTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tv_exifTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tv_exifTable.setHorizontalHeaderItem(1, item)
        self.tv_exifTable.horizontalHeader().setStretchLastSection(True)
        self.tv_exifTable.verticalHeader().setVisible(False)
        self.horizontalLayout_2.addWidget(self.tv_exifTable)

        self.retranslateUi(Tab)
        QtCore.QMetaObject.connectSlotsByName(Tab)

    def retranslateUi(self, Tab):
        _translate = QtCore.QCoreApplication.translate
        Tab.setWindowTitle(_translate("Tab", "Form"))
        self.btn_loadImage.setText(_translate("Tab", "Load Image.."))
        self.lb_image.setText(_translate("Tab", "Image"))
        self.lb_filename.setText(_translate("Tab", "filename"))
        item = self.tv_exifTable.horizontalHeaderItem(0)
        item.setText(_translate("Tab", "Property"))
        item = self.tv_exifTable.horizontalHeaderItem(1)
        item.setText(_translate("Tab", "Value"))

from widgets.ImageLabel import ImageLabel
