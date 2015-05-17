#!/usr/bin/env python
#encoding=utf-8

import os
import sys

DEBUG = True

# static paths
paths = {
    'root': '',
    'library': '',
    'tmp': '',
}


def setupPaths():
    path = sys.path[0]
    # 判断文件是编译后的文件还是脚本文件
    if os.path.isdir(path):  # 脚本文件目录
        exec_path = path
    else:  # 编译后的文件, 返回它的上一级目录
        exec_path = os.path.dirname(path)
    if DEBUG:
        print('running @ root path:', exec_path)
    paths['root'] = exec_path
    paths['library'] = os.path.join(exec_path, 'library')
    paths['tmp'] = os.path.join(exec_path, 'tmp')
    ensurePathsExist()


def ensurePathsExist():
    for _, path in paths.items():
        if not os.path.exists(path):
            os.makedirs(path)


def getTmpFilepath(filename):
    return os.path.join(paths['tmp'], os.path.basename(filename))


def getLibFilepath(filename):
    return os.path.join(paths['library'], os.path.basename(filename))


def moveToLibrary(filepath):
    libpath = os.path.join(
        paths['library'], os.path.basename(filepath)
    )
    os.rename(filepath, libpath)
    return libpath
