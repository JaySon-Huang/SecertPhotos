# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/ui_MainWindow.ui'
#
# Created: Tue Jun  9 22:51:45 2015
#      by: PyQt5 UI code generator 5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1036, 712)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setElideMode(QtCore.Qt.ElideMiddle)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_viewLibrary = LibraryTab()
        self.tab_viewLibrary.setObjectName("tab_viewLibrary")
        self.tabWidget.addTab(self.tab_viewLibrary, "")
        self.tab_addPhoto = AddPhotoTab()
        self.tab_addPhoto.setObjectName("tab_addPhoto")
        self.tabWidget.addTab(self.tab_addPhoto, "")
        self.tab_comparePhoto = ComparePhotoTab()
        self.tab_comparePhoto.setObjectName("tab_comparePhoto")
        self.tabWidget.addTab(self.tab_comparePhoto, "")
        self.tab_viewExif = ViewExifTab()
        self.tab_viewExif.setObjectName("tab_viewExif")
        self.tabWidget.addTab(self.tab_viewExif, "")
        self.horizontalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1036, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SecretPhotos"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_viewLibrary), _translate("MainWindow", "Library"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_addPhoto), _translate("MainWindow", "Add Photo"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_comparePhoto), _translate("MainWindow", "Compare Photo"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_viewExif), _translate("MainWindow", "Exif Infos"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuAbout.setTitle(_translate("MainWindow", "About"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setStatusTip(_translate("MainWindow", "Quit SecretPhotos"))
        self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionOpen.setStatusTip(_translate("MainWindow", "Open file..."))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+F"))

from widgets.AddPhotoTab import AddPhotoTab
from widgets.ViewExifTab import ViewExifTab
from widgets.ComparePhotoTab import ComparePhotoTab
from widgets.LibraryTab import LibraryTab
