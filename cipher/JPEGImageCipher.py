#!/usr/bin/env python3
#encoding=utf-8

'''
定义一个类似`接口`的存在
'''


class Base_JPEGImageCipher(object):

    def encrypt(self, image):
        '''返回一个加密之后的JPEGImage对象
        '''
        raise NotImplementedError

    def decrypt(self, image):
        '''返回一个解密之后的JPEGImage对象
        '''
        raise NotImplementedError

    def encrtptAndEmbData(self, image, data=b'Attack at dawn!'):
        '''返回一个嵌入信息并加密之后的JPEGImage对象
        '''
        raise NotImplementedError

    def embData(self, image, data):
        '''返回一个嵌入信息之后的JPEGImage对象
        '''
        raise NotImplementedError

    def extractData(self, image):
        '''返回提取到的信息
        '''
        raise NotImplementedError

    def decryptAndExtractData(self, image):
        '''返回解密后的图像以及提取到的信息
        '''
        raise NotImplementedError
