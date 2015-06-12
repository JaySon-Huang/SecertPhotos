#!/usr/bin/env python3
#encoding=utf-8

'''
定义一个类似`接口`的存在
'''
import math

from pyjpegtbx.constants import DCTSIZE2
from .utils import exgcd, multiplicative_inver, pow_mod


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



class FixedLogisticShuffeler(object):

    def __init__(self, seed):
        '''x0: (0, 1) without 0.5'''
        self.seed = seed

    def next(self):
        self.seed = 4 * self.seed * (1-self.seed)
        return 2 / math.pi * math.asin(math.sqrt(self.seed))

    def shuffle(self, lst):
        k = len(lst)-1
        while k > 0:
            ind = int(k*self.next())
            tmp = lst[k]
            lst[k] = lst[ind]
            lst[ind] = tmp
            k -= 1


class JPEGImageCipher0(object):
    '''
    广义Arnold变换方法, 默认为典型Arnold变换(猫映射)
    default :(a, b)   (1, 1)
             (c, d) = (1, 2)
    '''

    MAX_NBITS_MESSAGE_LENGTH = 16
    MAX_MESSAGE_LENGTH = (1 << MAX_NBITS_MESSAGE_LENGTH)-1

    def __init__(self, seed=0.362, abcd=(1, 1, 1, 2), sqrtN=8):
        '''
        abcd: 4-int-tuple
        sqrtN: sqrt of N
        '''
        super().__init__()
        self.a, self.b, self.c, self.d = abcd
        self.sqrtN = sqrtN
        gcd, _, _ = exgcd(self.a*self.d - self.b*self.c, sqrtN*sqrtN)
        if gcd != 1:
            raise ValueError("Must satisfy gcd(ad-bc, N)=1")
        self.shuffler = FixedLogisticShuffeler(seed)

    def encrypt(self, image):
        '''返回一个加密之后的JPEGImage对象
        '''
        ec_image = image.copy()
        for com in range(3):
            for i, block in enumerate(ec_image.data[com]):
                block = self.scrambledBlock(block)
                ec_image.data[com][i] = block
            ec_image.data[com] = self.shuffledComponemt(ec_image.data[com])
        return ec_image

    def scrambledBlock(self, block):
        res = [0] * (self.sqrtN * self.sqrtN)
        for x in range(self.sqrtN):
            for y in range(self.sqrtN):
                xx = (self.a * x + self.b * y) % self.sqrtN
                yy = (self.c * x + self.d * y) % self.sqrtN
                res[xx*self.sqrtN+yy] = block[x*self.sqrtN+y]
        return res

    def shuffledComponemt(self, comp):
        length = len(comp)
        ptrlst = [_ for _ in range(length)]
        self.shuffler.shuffle(ptrlst)
        ncomp = [None] * length
        for i, block in enumerate(comp):
            ncomp[i] = comp[ptrlst[i]]
        return ncomp

    def decrypt(self, image):
        '''返回一个解密之后的JPEGImage对象
        '''
        dc_image = image.copy()
        for com in range(3):
            for i, block in enumerate(dc_image.data[com]):
                block = self.unscrambledBlock(block)
                dc_image.data[com][i] = block
            dc_image.data[com] = self.unshuffledComponemt(dc_image.data[com])
        return dc_image

    def unscrambledBlock(self, block):
        res = [0] * (self.sqrtN * self.sqrtN)
        inver = multiplicative_inver(
            self.a*self.d-self.b*self.c, self.sqrtN
        )
        for x in range(self.sqrtN):
            for y in range(self.sqrtN):
                xx = inver*(self.d * x - self.b * y) % self.sqrtN
                yy = inver*(-self.c * x + self.a * y) % self.sqrtN
                res[xx*self.sqrtN+yy] = block[x*self.sqrtN+y]
        return res

    def unshuffledComponemt(self, comp):
        length = len(comp)
        ptrlst = [_ for _ in range(length)]
        self.shuffler.shuffle(ptrlst)
        ncomp = [None] * length
        for i, block in enumerate(comp):
            ncomp[ptrlst[i]] = comp[i]
        return ncomp

    def encrtptAndEmbData(self, image, data=b'Attack at dawn!'):
        image = self.encrypt(image)
        self.embData(image, data)
        return image

    def embData(self, image, data):
        length = len(data) * 8
        # 使用 MAX_NBITS_MESSAGE_LENGTH 个bit来存储长度信息
        # 最多可以存储 MAX_MESSAGE_LENGTH 长度的信息
        assert length < self.MAX_MESSAGE_LENGTH, \
            "嵌入数据量太大: %d(MAX: %d)" % (length, self.MAX_MESSAGE_LENGTH)
        # _id = image.comp_infos[0]['component_id']
        # _index = image.comp_infos[0]['component_index']
        # hist0 = ColorSpaceHistorgram(_id, image.data[_index])
        # print('embData   before', hist0.at(1))
        pos_infos = self.__shiftData(0, image, length)
        # _id = image.comp_infos[0]['component_id']
        # _index = image.comp_infos[0]['component_index']
        # hist1 = ColorSpaceHistorgram(_id, image.data[_index])
        bs = BitInputStream(data)
        pos_infos_index = 0
        for i in range(self.MAX_NBITS_MESSAGE_LENGTH):
            bit = 1 if (length & (0x01 << i)) > 0 else 0
            _index, coef_index, val_index, ori = pos_infos[pos_infos_index]
            if bit == 0:
                image.data[_index][coef_index][val_index] = ori - 1
            elif bit == 1:
                image.data[_index][coef_index][val_index] = ori + 1
            pos_infos_index += 1
        for bit in bs.read():
            _index, coef_index, val_index, ori = pos_infos[pos_infos_index]
            if bit == 0:
                image.data[_index][coef_index][val_index] = ori-1
            elif bit == 1:
                image.data[_index][coef_index][val_index] = ori+1
            pos_infos_index += 1
        # _id = image.comp_infos[0]['component_id']
        # _index = image.comp_infos[0]['component_index']
        # hist2 = ColorSpaceHistorgram(_id, image.data[_index])
        # print('embData   after ', hist2.at(1))

    def __shiftData(self, cindex, image, need):
        _id = image.comp_infos[cindex]['component_id']
        _index = image.comp_infos[cindex]['component_index']
        hist = ColorSpaceHistorgram(_id, image.data[_index])
        pos_infos = []
        nalloc = 0
        for val_index in range(1, DCTSIZE2):
            for coef_index, coef_block in enumerate(image.data[_index]):
                topVal, topNum = hist.top(val_index)
                # TODO: 没有处理使用多个slot嵌入数据的功能, 导致可嵌入数据量较少
                # 50% 也有待商榷?
                assert int(topNum*0.5) > need, \
                    "嵌入数据量太大: %d(MAX: %d)" % (need, )
                val = coef_block[val_index]
                if val < topVal:
                    coef_block[val_index] -= 1
                elif val > topVal:
                    coef_block[val_index] += 1
                else:  # 峰值位置, 记录可平移位置信息
                    pos_infos.append((_index, coef_index, val_index, topVal))
                    nalloc += 1

            return pos_infos

    def extractData(self, image):
        _id = image.comp_infos[0]['component_id']
        _index = image.comp_infos[0]['component_index']
        hist = ColorSpaceHistorgram(_id, image.data[_index])
        bout = BitOutputStream()
        isGettingMsg = False
        try:
            for val_index in range(1, DCTSIZE2):
                for coef_index, coef_block in enumerate(image.data[_index]):
                    topVal, _ = hist.top(val_index)
                    val = coef_block[val_index]
                    if val == topVal - 1:
                        bout.write(0)
                    elif val == topVal + 1:
                        bout.write(1)

                    if not isGettingMsg:
                        if len(bout) == 16:
                            # 前MAX_NBITS_MESSAGE_LENGTH bit存储嵌入了多长的数据
                            emb_message_length = bout.getInt(
                                nbit=self.MAX_NBITS_MESSAGE_LENGTH
                            )
                            isGettingMsg = True
                    elif len(bout) == emb_message_length:
                        # 已经获取全部嵌入数据
                        raise Exception
        except Exception:
            pass

        msg = bytearray(bout._bytes)
        return msg

    def clearData(self, image):
        _id = image.comp_infos[0]['component_id']
        _index = image.comp_infos[0]['component_index']
        hist = ColorSpaceHistorgram(_id, image.data[_index])
        # print('clearData before', hist.at(1))
        hasGetLength = False
        bout = BitOutputStream()
        for val_index in range(1, DCTSIZE2):
            for coef_block in image.data[_index]:
                topVal, _ = hist.top(val_index)
                val = coef_block[val_index]
                if val == topVal - 1:
                    bout.write(0)
                elif val == topVal + 1:
                    bout.write(1)

                if val < topVal:
                    coef_block[val_index] += 1
                elif val > topVal:
                    coef_block[val_index] -= 1

                if not hasGetLength:
                    if len(bout) == 16:  # 前16bit用来存储嵌入了多长的数据
                        emb_message_length = bout.getInt(
                            nbit=self.MAX_NBITS_MESSAGE_LENGTH
                        )
                        hasGetLength = True
            # TODO: 没有处理使用多个slot嵌入数据的功能
            # if hasGetLength and emb_message_length < :
            break
        # hist1 = ColorSpaceHistorgram(_id, image.data[_index])
        # print('clearData after ', hist1.at(1))

    def decryptAndExtractData(self, image):
        bdata = self.extractData(image)
        self.clearData(image)
        image = self.decrypt(image)
        return image, bdata


class JPEGImageCipher1(JPEGImageCipher0):
    def __init__(self, seed=0.362):
        super().__init__(seed)
        self.k = 24
        self.p = 2
        self.r = 300

    def f(self, x):
        return self.k * (x ** self.p) + self.r

    def scrambledBlock(self, block):
        res = [0] * (self.sqrtN * self.sqrtN)
        for x in range(self.sqrtN):
            for y in range(self.sqrtN):
                xx = (self.a * x + self.b * y) % self.sqrtN
                yy = (self.c * x + self.d * y + self.f(xx)) % self.sqrtN
                res[xx*self.sqrtN+yy] = block[x*self.sqrtN+y]
        return res

    def unscrambledBlock(self, block):
        res = [0] * (self.sqrtN * self.sqrtN)
        inver = int(multiplicative_inver(self.a*self.d-self.b*self.c, self.sqrtN))
        for x in range(self.sqrtN):
            fx = self.f(x)
            for y in range(self.sqrtN):
                xx = inver*(self.d * x - self.b * (y - fx)) % self.sqrtN
                yy = inver*(-self.c * x + self.a * (y - fx)) % self.sqrtN
                res[xx*self.sqrtN+yy] = block[x*self.sqrtN+y]
        return res


class JPEGImageCipher2(JPEGImageCipher1):
    def f(self, x, mod):
        # return (self.k * pow_mod(x, self.p, mod) + self.r) % mod
        return (self.k * ((x**self.p) % mod) + self.r) % mod

    def scrambledBlock(self, block):
        res = [0] * (self.sqrtN * self.sqrtN)
        for x in range(self.sqrtN):
            for y in range(self.sqrtN):
                xx = (self.a * x + self.b * y) % self.sqrtN
                yy = (self.c * x + self.d * y + self.f(xx, self.sqrtN)) % self.sqrtN
                res[xx*self.sqrtN+yy] = block[x*self.sqrtN+y]
        return res

    def unscrambledBlock(self, block):
        res = [0] * (self.sqrtN * self.sqrtN)
        inver = int(multiplicative_inver(self.a*self.d-self.b*self.c, self.sqrtN))
        for x in range(self.sqrtN):
            fx = self.f(x, self.sqrtN)
            for y in range(self.sqrtN):
                xx = inver*(self.d * x - self.b * (y - fx)) % self.sqrtN
                yy = inver*(-self.c * x + self.a * (y - fx)) % self.sqrtN
                res[xx*self.sqrtN+yy] = block[x*self.sqrtN+y]
        return res


class ColorSpaceHistorgram(object):
    def __init__(self, cid, component_datas):
        self.slots = [None] * DCTSIZE2
        for coef_block in component_datas:
            for i, val in enumerate(coef_block):
                if not self.slots[i]:
                    self.slots[i] = {}
                self.slots[i][val] = self.slots[i].get(val, 0) + 1

    def min_max(self, slot_index=None):
        '''slot_index=None:返回所有slot的min、max值
        如果指定slot_index, 则返回该slot的min、max值
        '''
        try:
            _ = self._min_max_vals
        except AttributeError:
            ret = []
            for slot in self.slots:
                keys = slot.keys()
                ret.append((min(keys), max(keys)))
            self._min_max_vals = tuple(ret)
        finally:
            if slot_index is None:
                return self._min_max_vals
            else:
                return self._min_max_vals[slot_index]

    def top(self, slot_index=None):
        try:
            _ = self._topVals
        except AttributeError:
            ret = []
            for slot in self.slots:
                items = sorted(slot.items(), key=lambda pair: pair[1])
                ret.append(items[-1])
            self._topVals = tuple(ret)
        finally:
            if slot_index is None:
                return self._topVals
            else:
                return self._topVals[slot_index]

    def at(self, slot_index):
        return sorted(self.slots[slot_index].items())

    def __str__(self):
        lst = []
        for i, slot in enumerate(self.slots):
            keys = slot.keys()
            maxVal, minVal = max(keys), min(keys)
            items = sorted(slot.items(), key=lambda pair: pair[1])
            topPos, topVal = items[-1]
            lst.append(
                '''`%2d`: { [top @%2d:%5d] range: %4d ~ %4d }'''
                % (i, topPos, topVal, minVal, maxVal)
            )
        return '\n'.join(lst)

    def __repr__(self):
        return self.__str__()


class BitInputStream(object):
    def __init__(self, _bytes):
        self._bytes = _bytes

    def read(self):
        for ch in self._bytes:
            for i in range(8):
                yield 1 if (ch & (0x1 << i) > 0) else 0

    def __len__(self):
        return len(self._bytes) * 8


class BitOutputStream(object):
    def __init__(self):
        self._bytes = []
        self._curByte = 0
        self._curShift = 0

    def write(self, bit):
        self._curByte |= (bit << self._curShift)
        self._curShift += 1
        if self._curShift == 8:
            self._bytes.append(self._curByte)
            self._curByte = 0
            self._curShift = 0

    def hexdump(self):
        return ''.join(map(lambda x: '%02x' % x, self._bytes))

    def __len__(self):
        return len(self._bytes) * 8 + self._curShift

    def getInt(self, nbit=32):
        ret = 0
        for byte in reversed(self._bytes[:nbit//8]):
            ret <<= 8
            ret += byte
        self._bytes = self._bytes[nbit//8:]
        return ret


def encdec(img, cls):
    cipher = cls()
    encImg = cipher.encrypt(img)
    # cipher = cls()
    # decImg = cipher.decrypt(encImg)


def main():
    ## 图片加密解密的基本case
    # from pyjpegtbx import JPEGImage
    # img = JPEGImage.open('../sos.jpg')
    # cipher = JPEGImageCipher2()
    # encImg = cipher.encrypt(img)
    # encImg.save('lfs_enc.jpg')
    # cipher = JPEGImageCipher2()
    # decImg = cipher.decrypt(encImg)
    # decImg.save('lfs_dec.jpg')

    # rg = FixedLogisticShuffeler(0.500001)
    ## 混沌序列的结果
    # for _ in range(100):
    #     print(rg.next())
    ## 利用混沌序列进行置乱和恢复
    # length = 100
    # target = [_ for _ in range(length)]
    # enc = [0] * length
    # dec = [0] * length
    # ptrlst = [_ for _ in range(length)]
    # print('ori', target)
    # rg.shuffle(ptrlst)
    # print('ptr', ptrlst)
    # for x in range(length):
    #     enc[x] = target[ptrlst[x]]
    # print('enc', enc)
    # for x in range(length):
    #     dec[ptrlst[x]] = enc[x]
    # print('dec', dec)

    ## 三种图像加密方式的时间对比
    # import time
    # from pyjpegtbx import JPEGImage
    # img = JPEGImage('sos.jpg')
    # clses = [JPEGImageCipher0, JPEGImageCipher1, JPEGImageCipher2]
    # for cls in clses:
    #     beg = time.time()
    #     encdec(img, cls)
    #     end = time.time()
    #     print("Time for %s:%f" % (cls, end - beg))

    ## 快速幂和`**`运算的时间对比
    # import time
    # run_round = 100000
    # for i in range(2):
    #     beg = time.time()
    #     if i == 0:
    #         for x in range(run_round):
    #             p = (x**20) % 1007
    #         print(p)
    #     elif i == 1:
    #         for x in range(run_round):
    #             p = pow_mod(x, 20, 1007)
    #         print(p)
    #     end = time.time()
    #     print("Time :%f" % (end - beg))

    ## 直方图功能函数测试
    # from pyjpegtbx import JPEGImage
    # img = JPEGImage.open('../lfs.jpg')
    # historgrams = []
    # for comp_info in img.comp_infos:
    #     _id = comp_info['component_id']
    #     _index = comp_info['component_index']
    #     historgrams.append(
    #         ColorSpaceHistorgram(
    #             _id, img.data[_index]
    #         )
    #     )
    # import IPython
    # IPython.embed()
    # print(historgrams[0].top())
    # print(historgrams[0].min_max())
    # print(str(historgrams[0]))
    # print(str(historgrams[0].at(0)))
    ## 位流的测试
    # bs = BitInputStream(b'\xff\x01\x30')
    # for i, bit in enumerate(bs.read()):
    #     print(bit, end='')
    #     if i % 8 == 7:
    #         print()
    ## 图像隐写部分
    from pyjpegtbx import JPEGImage
    img = JPEGImage.open('../sos.jpg')
    cipher = JPEGImageCipher0()
    encImg = cipher.encrtptAndEmbData(img, '冰菓如茶'.encode('utf-8'))
    encImg.save('lfs_enc.jpg')
    cipher = JPEGImageCipher0()
    decImg, data = cipher.decryptAndExtractData(encImg)
    decImg.save('lfs_dec.jpg')

    print(data.decode('utf-8'))

if __name__ == '__main__':
    main()
