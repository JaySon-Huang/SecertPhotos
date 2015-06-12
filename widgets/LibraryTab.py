#!/usr/bin/env python3
#encoding=utf-8

'''
显示Library文件夹下图片
'''
import os

from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, QSizePolicy

from .ui_LibraryTab import Ui_Tab
from .GridWidget import GridWidget
from utils import getPasswordInput
from utils.logUtils import Log


class LibraryTab(QWidget, Ui_Tab):
    # property
    columnSize = 3
    # signals
    passwordEntered = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        # setup widgets
        self.setupUi(self)

        self.btn_enterPassword.clicked.connect(
            self.btn_enterPassword_clicked
        )

    @pyqtSlot()
    def btn_enterPassword_clicked(self):
        password, isOK = getPasswordInput(self)
        if isOK:
            Log.d('Password is:{}'.format(password))
            self.passwordEntered.emit(password)

    def setLibraryPath(self, libpath):
        self.libpath = libpath

    def refresh(self):
        libfiles = []
        for filename in os.listdir(self.libpath):
            if filename.endswith('jpeg') or filename.endswith('.jpg'):
                libfiles.append(os.path.join(self.libpath, filename))
        Log.i('files in library:{}'.format(libfiles))

        self.libraryWidgets = []

        sp = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sp.setHorizontalStretch(0)
        sp.setVerticalStretch(0)

        i = -1  # init i in case of libfiles is []
        for i, filepath in enumerate(libfiles):
            col = i % self.columnSize
            row = i // self.columnSize
            widget = GridWidget(self.scrollAreaWidgetContents)
            sp.setHeightForWidth(widget.sizePolicy().hasHeightForWidth())
            widget.setSizePolicy(sp)
            widget.setContent(filepath, (250, 250))
            self.gridLayout.addWidget(
                widget, row, col, Qt.AlignHCenter | Qt.AlignVCenter
            )
            self.libraryWidgets.append(widget)
        while i < 11:
            i += 1
            col = i % self.columnSize
            row = i // self.columnSize
            widget = GridWidget(self.scrollAreaWidgetContents)
            sp.setHeightForWidth(widget.sizePolicy().hasHeightForWidth())
            widget.setSizePolicy(sp)
            widget.setContent('', None)
            self.gridLayout.addWidget(
                widget, row, col, Qt.AlignHCenter | Qt.AlignVCenter
            )
            self.libraryWidgets.append(widget)
