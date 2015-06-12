#!/usr/bin/env python3
#encoding=utf-8

'''
把图片进行加密/解密、嵌入/提取信息、添加到Library的Tab
'''
from functools import partial

from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, QFileDialog, QInputDialog, QLineEdit, QSizePolicy
from pyjpegtbx import JPEGImage

from .ui_AddPhotoTab import Ui_Tab
from utils import runtime, getPasswordInput, strings, password2seed
from utils.fileUtils import (
    paths, getTmpFilepath, getLibFilepath, moveToLibrary
)
from utils.logUtils import Log
from cipher.JPEGImageCipher import JPEGImageCipher1 as JPEGImageCipher
# from cipher.JPEGImageCipher import JPEGImageCipher0 as JPEGImageCipher


class AddPhotoTab(QWidget, Ui_Tab):
    # signals
    passwordEntered = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        # setup widgets
        self.setupUi(self)
        self.connectSlots()

        # 设置显示的字符串
        self.saContents_ori.setTitle('Original')
        self.saContents_dst.setTitle('Destination')
        self.lb_msg.setText('')
        # 更新当前是否同步滚动
        self.setScrollMode(self.ckbox_scrollMode.checkState())

    def connectSlots(self):
        # 设置是否同步滚动
        self.ckbox_scrollMode.stateChanged['int'].connect(
            self.setScrollMode
        )
        # 载入图片成功, 使按钮可用
        self.saContents_ori.imageLoaded.connect(
            partial(self.setBtnEnable, enable=True)
        )
        # 清除图片, 使按钮不可用
        self.saContents_ori.imageCleared.connect(
            partial(self.setBtnEnable, enable=False)
        )

        self.btn_loadImage.clicked.connect(
            self.btn_loadImage_clicked
        )
        self.btn_saveToLibrary.clicked.connect(
            self.btn_saveToLibrary_clicked
        )
        self.btn_encrypt.clicked.connect(
            partial(self.encryptPhoto, toEmbMessage=False)
        )
        self.btn_decrypt.clicked.connect(
            partial(self.decryptPhoto, toExtractMessage=False)
        )
        self.btn_encryptEmb.clicked.connect(
            partial(self.encryptPhoto, toEmbMessage=True)
        )
        self.btn_decryptExtract.clicked.connect(
            partial(self.decryptPhoto, toExtractMessage=True)
        )

    @pyqtSlot(bool)
    def setBtnEnable(self, enable):
        # 成功载入后, 把 Encrypt/Decrypt 按钮设置为enable状态
        self.btn_encrypt.setEnabled(enable)
        self.btn_decrypt.setEnabled(enable)
        self.btn_encryptEmb.setEnabled(enable)
        self.btn_decryptExtract.setEnabled(enable)

    @pyqtSlot(int)
    def setScrollMode(self, state):
        if state == Qt.Unchecked:
            self.ui.scrollArea_ori.verticalScrollBar().valueChanged['int'].disconnect(
                self.scrollArea_dst.verticalScrollBar().setValue
            )
            self.scrollArea_dst.verticalScrollBar().valueChanged['int'].disconnect(
                self.scrollArea_ori.verticalScrollBar().setValue
            )
        elif state == Qt.Checked:
            self.scrollArea_ori.verticalScrollBar().valueChanged['int'].connect(
                self.scrollArea_dst.verticalScrollBar().setValue
            )
            self.scrollArea_dst.verticalScrollBar().valueChanged['int'].connect(
                self.scrollArea_ori.verticalScrollBar().setValue
            )

    @pyqtSlot()
    def btn_loadImage_clicked(self):
        filepath, _ = QFileDialog.getOpenFileName(
            parent=self, caption='Open', directory='', filter='*.jpg'
        )
        if filepath:
            # clear and then set ori side
            self.__loadOriPhoto(filepath=filepath, clear=True)
            # clear dst side
            self.__loadDstPhoto(clear=True)

    @pyqtSlot(bool)
    def encryptPhoto(self, toEmbMessage):
        if not runtime['seed']:
            password, isOK = getPasswordInput(self)
            if not isOK:  # 取消输入密码
                return
            else:
                self.passwordEntered.emit(password)
                runtime['seed'] = password2seed(password)

        cipher = JPEGImageCipher(runtime['seed'])
        if toEmbMessage:
            msg, isOK = QInputDialog.getMultiLineText(
                self, 'Enter the message you want to emb',
                'Message:'
            )
            bdata = msg.encode('utf-8')  # str -> bytes
            Log.i('get `{}`<=>`{}` from input dialog'.format(msg, bdata))
            img = cipher.encrtptAndEmbData(runtime['ori']['image'], bdata)
            self.__loadDstPhoto(img=img, msg=msg, clear=True)
        else:
            img = cipher.encrypt(runtime['ori']['image'])
            self.__loadDstPhoto(img=img, clear=True)
        ## 先保存临时文件, 再载入临时文件显示图片 (FIXME: 多次修改,可能有bug)##
        # tmpFilepath = self.__saveToTempFile(img, img.filename)
        # self.__loadDstPhoto(self, filepath=tmpFilepath)
        ## 直接通过JPEGImage对象的接口中载入图像数据 ##

    @pyqtSlot(bool)
    def decryptPhoto(self, toExtractMessage):
        if not runtime['seed']:
            password, isOK = getPasswordInput(self)
            if not isOK:  # 取消输入密码
                return
            else:
                self.passwordEntered.emit(password)
                runtime['seed'] = password2seed(password)

        cipher = JPEGImageCipher(runtime['seed'])
        if toExtractMessage:
            img, bdata = cipher.decryptAndExtractData(runtime['ori']['image'])
            msg = bdata.decode('utf-8')  # bytes -> str
            Log.i('The message extract is:`{}`<=>`{}`'.format(bdata, msg))
            self.lb_msg.setText(
                strings['format']['extract'] % msg
            )
            self.__loadDstPhoto(img=img, msg=msg, clear=True)
        else:
            img = cipher.decrypt(runtime['ori']['image'])
            self.__loadDstPhoto(img=img, clear=True)
        ## 先保存临时文件, 再载入临时文件显示图片 ##
        # tmpFilepath = self.__saveToTempFile(img, img.filename)
        # self.__loadDstPhoto(filepath=tmpFilepath)
        ## 直接通过JPEGImage对象的接口中载入图像数据 ##

    @pyqtSlot()
    def btn_saveToLibrary_clicked(self):
        ## 使用临时文件存储的方式, 直接移动文件 ## FIXME: 接口大幅修改过, 下面的代码有bug
        # libpath = moveToLibrary(runtime['dst']['filepath'])
        # print('file: %s moved to %s' % (self.loaded['dstFilepath'], libpath))
        # runtime['dst']['filepath'] = libpath
        # runtime['dst']['image'].filename = libpath
        ## 把结果图片保存到`paths.library`中 ##
        filepath = getLibFilepath(runtime['ori']['filepath'])
        runtime['dst']['filepath'] = filepath
        runtime['dst']['image'].save(filepath)

    def __loadOriPhoto(self, *, filepath=None, img=None, msg='', clear=False):
        '''
        @filepath   : 文件路径
        @img        : 图像对象
        @clear      : 清除
        从filepath或者img参数中设置ori位置的图片
        '''
        self.lb_msg.setText(msg)
        if clear:
            runtime['ori']['filepath'] = None
            runtime['ori']['image'] = None
            self.saContents_ori.clear()

        if filepath:
            img = JPEGImage.open(filepath)
            self.saContents_ori.setImage(img)
            runtime['ori']['filepath'] = filepath
            runtime['ori']['image'] = img
        elif img:
            self.saContents_ori.setImage(img)
            runtime['dst']['filepath'] = None
            runtime['dst']['image'] = img
        else:
            return

    def __loadDstPhoto(self, *, filepath=None, img=None, msg='', clear=False):
        '''
        @filepath   : 文件路径
        @img        : 图像对象
        @clear      : 清除
        从filepath或者img参数中设置dst位置的图片
        '''
        self.lb_msg.setText(msg)
        if clear:
            runtime['dst']['filepath'] = None
            runtime['dst']['image'] = None
            self.saContents_dst.clear()
            # 清除载入图片后, 把saveToLibrary设为不可用
            self.btn_saveToLibrary.setEnabled(False)

        if filepath:
            img = JPEGImage.open(filepath)
            self.saContents_dst.setImage(img)
            runtime['dst']['filepath'] = filepath
            runtime['dst']['image'] = img
        elif img:
            self.saContents_dst.setImage(img)
            runtime['dst']['filepath'] = None
            runtime['dst']['image'] = img
        else:
            return
        # 成功载入图片后, 把saveToLibrary设为可用
        self.btn_saveToLibrary.setEnabled(True)

    # def __saveToTempFile(self, img, filename):
    #     '''
    #     @img        : 图片对象
    #     @filename   : 保存的文件名
    #     保存img对象中存储的图像到`tmp`文件夹下,
    #     '''
    #     filepath = getTmpFilepath(filename)
    #     print(
    #         'save encrypted/decrypted image to temp file:',
    #         filepath
    #     )
    #     img.save(filepath)
    #     return filepath
