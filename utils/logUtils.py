#!/usr/bin/env python
#encoding=utf-8

import logging

from . import DEBUG


class Log(object):
    logger = None
    log_filename = 'last.log'
    fmt = '[%(levelname)8s] %(asctime)s - %(message)s '
    datefmt = '%m-%d %H:%M'

    @staticmethod
    def init():
        logging.basicConfig(
            level=logging.DEBUG if DEBUG else logging.INFO,
            format=Log.fmt, datefmt=Log.datefmt
        )
        Log.logger = logging.getLogger('SecretPhotos')

        f_handler = logging.FileHandler(Log.log_filename)
        f_handler.setLevel(logging.INFO)
        f_handler.setFormatter(logging.Formatter(fmt=Log.fmt, datefmt=Log.datefmt))
        Log.logger.addHandler(f_handler)

    @staticmethod
    def d(msg):
        Log.logger.debug(msg)

    @staticmethod
    def i(msg):
        Log.logger.info(msg)

    @staticmethod
    def w(msg):
        Log.logger.warning(msg)

    @staticmethod
    def e(msg):
        Log.logger.error(msg)
