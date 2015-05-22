#!/usr/bin/env python3
#encoding=utf-8

import os
from PyQt5.QtWidgets import QWidget, QFileDialog, QTableWidgetItem
from pyjpegtbx import JPEGImage

from .ui_ViewExifTab import Ui_Tab


class ViewExifTab(QWidget, Ui_Tab):
    def __init__(self, parent=None):
        super().__init__(parent)
        # setup widgets
        self.setupUi(self)

        self.imagePath = None

        self.btn_loadImage.clicked.connect(
            self.on_loadImage_clicked
        )

    def on_loadImage_clicked(self):
        filepath, _ = QFileDialog.getOpenFileName(
            parent=self, caption='Open', directory='', filter='*.jpg'
        )
        if filepath:
            self.imagePath = filepath
            self.lb_image.setImageFileSrc(filepath, 400, 400)
            self.lb_filename.setText(
                os.path.basename(filepath)
            )

            img = JPEGImage.open(filepath)
            exif_info = img.get_exif()
            self.resetExif()
            self.updateExif(exif_info)

    def resetExif(self):
        self.tv_exifTable.clearContents()
        # self.tv_exifTable.setHorizontalHeaderLabels(["Property", "Value"])
        while self.tv_exifTable.rowCount():
            self.tv_exifTable.removeRow(0)

    def updateExif(self, exif_info):
        # update tv_exifTable
        row = 0
        for key, entries in exif_info.items():
            self.tv_exifTable.insertRow(row)
            item = QTableWidgetItem(key)
            self.tv_exifTable.setItem(row, 0, item)
            # print(key, '->', item)
            self.tv_exifTable.setSpan(row, 0, 1, 2)
            row += 1
            for entry in entries:
                _type, fmt, ncomp, comps = entry
                # print(entry)
                self.tv_exifTable.insertRow(row)
                # type
                item = QTableWidgetItem(str(_type))
                self.tv_exifTable.setItem(row, 0, item)
                if _type.id in (0x9000, 0xa000):
                    item = QTableWidgetItem(comps.decode('ascii'))
                elif _type.id == 0x9101:
                    s = ''
                    for b in comps:
                        s += {
                            4: 'R', 5: 'G', 6: 'B',
                            1: 'Y', 2: 'Cr', 3: 'Cb',
                            0: '',
                        }[b]
                    item = QTableWidgetItem(s)
                else:  # val
                    item = QTableWidgetItem(str(comps))
                self.tv_exifTable.setItem(row, 1, item)
                row += 1
b'ACD Systems \xca\xfd\xc2\xeb\xb3\xc9\xcf\xf1\x00'
