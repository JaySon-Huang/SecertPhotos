#!/usr/bin/env python3
#encoding=utf-8

import sys

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import (
    QApplication, QMainWindow,
)

from widgets.ui_MainWindow import Ui_MainWindow
from utils import (
    password2seed, runtime
)
from utils.fileUtils import (
    paths, setupPaths
)
from utils.logUtils import Log

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
        Log.i('MainWindow setup.')

    def setUpTabLibrary(self, ui):
        ui.tabWidget.currentChanged.connect(
            self.on_selected_tab_changed
        )

        ui.tab_viewLibrary.setLibraryPath(paths['library'])
        ui.tab_viewLibrary.refresh()
        ui.tab_viewLibrary.passwordEntered.connect(
            self.setSeed
        )

    @pyqtSlot(str)
    def setSeed(self, pwd):
        runtime['seed'] = password2seed(pwd)

    @pyqtSlot(int)
    def on_selected_tab_changed(self, index):
        if index == 0:
            self.ui.tab_viewLibrary.refresh()


def main():
    Log.init()
    setupPaths()

    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
