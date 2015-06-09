#!/usr/bin/env python
#encoding=utf-8
import hashlib


def password2seed(password):
    '''
    字符串形式的password变为0.0~1.0的seed值
    '''
    h = hashlib.md5(password.encode('utf-8')).digest()
    front, back = 0, 0
    for i, num in enumerate(h):
        if i < 8:
            front <<= 8
            front += num
            front &= 0xFFFFFFFF
        else:
            back <<= 8
            back += num
            back &= 0xFFFFFFFF
    front *= 1.0
    back *= 1.0
    seed = front/back if front < back else back/front
    return seed
