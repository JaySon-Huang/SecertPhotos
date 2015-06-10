#!/usr/bin/env python3
#encoding=utf-8

import sys

from PyQt5.QtCore import (
    QDir, Qt, QVariant, pyqtSlot
)
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QItemDelegate, QLabel, QHeaderView, QGridLayout,
    QWidget, QScrollArea, QGraphicsWidget, QFileDialog, QTreeWidgetItem,
    QSizePolicy, QInputDialog, QLineEdit
)
from PyQt5.QtGui import (
    QPixmap, QStandardItemModel, QStandardItem
)

from widgets.ui_MainWindow import Ui_MainWindow
from utils import password2seed
from utils.fileUtils import (
    paths, setupPaths
)

pics = ['lfs.jpg', 'tmp0.jpg', 'tmp1.jpg']


class MainWindow(QMainWindow):
    '''Main Window of Secret Photo'''

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.loaded = {}
        self.seed = None

        self.setUpTabLibrary(self.ui)
        self.setUpTabAddPhoto(self.ui)

    def setUpTabLibrary(self, ui):
        ui.tabWidget.currentChanged.connect(
            self.on_selected_tab_changed
        )

        ui.tab_viewLibrary.setLibraryPath(paths['library'])
        ui.tab_viewLibrary.refresh()
        ui.tab_viewLibrary.passwordEntered.connect(
            self.setSeed
        )

    def setUpTabAddPhoto(self, ui):
        pass

    @pyqtSlot(str)
    def setSeed(self, pwd):
        self.seed = password2seed(pwd)

    @pyqtSlot(int)
    def on_selected_tab_changed(self, index):
        if index == 0:
            self.ui.tab_viewLibrary.refresh()


def main():
    setupPaths()

    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
