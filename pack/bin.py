# -*- coding: UTF-8 -*-
from pack.algorithm import *
from common.log import *
# 第三方算法库
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from struct import *


class Bin:
    def __init__(self, f, offset):
        if isinstance(f, bytearray) is False and isinstance(f, bytes) is False:
            info(f"Open file {f}")
            self.source = bytearray(open(f, 'rb').read())
        else:
            self.source = bytearray(f)
        self.content = bytearray(self.source)
        self.offset = offset

    def __add__(self, other):
        new_obj = None
        if self.offset < other.offset and self.offset + len(self.content) <= other.offset:
            new_obj = Bin(self.content + bytearray([0xFF] * (other.offset - len(self.content))) + other.content,
                          self.offset)
        elif other.offset < self.offset and other.offset + len(other.content) <= self.offset:
            new_obj = Bin(other.content + bytearray([0xFF] * (self.offset - len(other.content))) + self.content,
                          other.offset)
        else:
            error("Wrong offset")
        return new_obj

    def reset(self):
        """
        还原content: content = src_content
        :return: None
        """
        self.content = bytearray(self.source)

    def update(self):
        self.source = bytearray(self.content)

    def del_end_ff(self, alignment=4):
        """
        删除content结尾的0xFF
        :param alignment: 对齐字节，一般芯片都为4字节对齐
        :return: None
        """
        i = 0
        for i in reversed(range(0, len(self.content))):
            if self.content[i] != 0xFF:
                break
        return self.content[:i + alignment - i % alignment]

    def save(self, path):
        info(f"Save to {path}")
        new_file = open(path, 'wb')
        new_file.write(self.content)
        new_file.close()

    def fill_bytes(self, fill=0xFF, end=None, alignment=128):
        """
        填充字节
        :param fill: 填入字节
        :param end: 填充到的结尾
        :param alignment: 若end为None的情况下，填充到所定义对齐的位置
        :return: None
        """
        if end is not None and end % 2 == 0 and end >= len(self.content):
            fill_length = end - len(self.content)
        elif alignment % 2 == 0:
            fill_length = 128 - len(self.content) % 128
        else:
            error("Unknown end")
            return
        info(f"Fill 0xFF until {hex(len(self.content) + fill_length)}")
        self.content += bytearray([0xff] * fill_length)

    def write_length_bytes(self, offset, start=0, bytes_length=4, cover=True):
        """
        向指定offset处写入当前包大小
        :param start: 起始计算位置
        :param offset: 写入地址的偏移
        :param bytes_length: 长度所占字节长度
        :param cover: True-覆盖 False-插入
        :return: None
        """
        if offset > len(self.content)-4:
            error("Wrong offset")
            return
        info(f"Write length bytes to offset {hex(offset)} from {hex(start)}")
        length = len(self.content) - start
        if cover is True:
            for i in range(0, bytes_length):
                self.content[offset + i] = (length >> i*8) & 0xFF

    def crc32_update_revtab(self, offset, start, init=0xFFFFFFFF, cover=True):
        """
        计算CRC32, 使用revtab
        :param offset: 写入位置
        :param init: CRC32初始值
        :param start: 开始计算的起始位置
        :param cover: True-覆盖 False-插入
        :return: None
        """
        info(f"Calculate CRC32 from {hex(start)} and write to {hex(offset)}")
        crc = crc32_update_revtab(self.content[start:])
        if cover is True:
            for i in range(0, 4):
                self.content[offset + i] = (crc >> i * 8) & 0xFF

    def aes_ecb_encryptyion(self, key, start):
        if len(self.content) % 16 != 0:
            error("The length of bin is not the multiples of 16")
            return
        info(f"Encrypt with AES ECB from {hex(start)}")
        info(f"The key is {key}")
        encryptor = Cipher(
            algorithms.AES(bytes.fromhex(key)),
            modes.ECB(),
            backend=default_backend()
        ).encryptor()

        packages = int(len(self.content) / 16)
        for i in range(0, packages):
            self.content[start + 16*i: start + 16*(i+1)] = \
                encryptor.update(self.content[start + 16*i: start + 16*(i+1)])

    def bin2hex(self, path):
        fhex = open(path, 'w')
        offset = 0
        seg_addr = 0
        for i in range(0, int(len(self.content)/16)):
            checksum = 0
            result = ':'
            bindata = self.content[i*16: (i+1)*16]
            result += '%02X' % len(bindata)
            result += '%04X' % offset
            result += '00'
            checksum = len(bindata)
            checksum += (offset & 0xff) + (offset >> 8)

            for j in range(0, len(bindata)):
                byte = unpack('B', bytes([bindata[j]]))
                result += '%02X' % byte
                checksum += byte[0]

            checksum = 0x01 + ~checksum
            checksum = checksum & 0xff
            result += '%02X\n' % checksum
            fhex.write(result)
            offset += len(bindata)
            if offset == 0x10000:
                offset = 0
                seg_addr += 1
                result = ':02000004'
                result += '%02X%02X' % ((seg_addr >> 8) & 0xff, seg_addr & 0xff)
                checksum = 0x02 + 0x04 + (seg_addr >> 8) + seg_addr & 0xff
                checksum = -checksum
                result += '%02X' % (checksum & 0xff)
                result += '\n'
                fhex.write(result)
            # end if
            if len(bindata) < 0x10:
                break
        # end if
        # end while
        fhex.write(':00000001FF')
        fhex.close()



