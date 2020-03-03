# -*- coding: UTF-8 -*-
from common import *
import os
import shutil
import time


def pack(config):
    info("Start pack")
    info(f"Project: Camel")

    app1_ver_list = []
    app2_ver_list = []

    for key in config['IAR']['firmware']:
        # 创建文件夹
        ver1 = config['bin']['app1'][f"Legal-{key}"].content[0x0E: 0x10]
        ver1.reverse()
        app1_ver_list.append(ver1.hex())
        ver1_FF = bytearray(ver1)
        ver1_FF[1] = 0xFF
        ver2 = config['bin']['app2'][f"App-{key}"].content[0x0E: 0x10]
        ver2.reverse()
        app2_ver_list.append(ver2.hex())
        ver2_FF = bytearray(ver2)
        ver2_FF[1] = 0xFF
        tmp_path = f'./temp/Camel_03_{key}_Merged_V{ver1.hex()}-V{ver2.hex()}'
        os.makedirs(tmp_path)

        # 获取文件对象
        boot = config['bin']['boot'][config['IAR']['firmware'][key][0]]
        app1 = config['bin']['app1'][config['IAR']['firmware'][key][1]]
        app2 = config['bin']['app2'][config['IAR']['firmware'][key][2]]

        # 处理APP1
        # 填充0xFF
        app1.fill_bytes(fill=0xFF, end=None, alignment=128)
        # 写入包长字节到偏移0x08
        app1.write_length_bytes(offset=0x08)

        # 从0x0E开始计算CRC写入偏移0x04
        app1.crc32_update_revtab(offset=0x04, start=0x0E)
        # 更新文件供最后组包用
        app1.update()
        # 加密包, 从0x10地址开始
        app1.aes_ecb_encryptyion('5A435A66755436363669526467504E48', 0x10)
        # 从0x04开始计算CRC写入偏移0x00
        app1.crc32_update_revtab(offset=0x00, start=0x04)
        # 保存正式升级文件
        app1.save(f"{tmp_path}/Camel_03_KF13A017_{key}_APP1_V{ver1.hex()}.bin")

        # 还原文件
        app1.reset()
        # 修改版本号为0xFF
        app1.content[0x0E] = 0xFF
        # 从0x0E开始计算CRC写入偏移0x04
        app1.crc32_update_revtab(offset=0x04, start=0x0E)
        # 加密包, 从0x10地址开始
        app1.aes_ecb_encryptyion('5A435A66755436363669526467504E48', 0x10)
        # 从0x04开始计算CRC写入偏移0x00
        app1.crc32_update_revtab(offset=0x00, start=0x04)
        # 保存FF升级文件
        app1.save(f"{tmp_path}/Camel_03_KF13A017_{key}_APP1_V{ver1_FF.hex().upper()}.bin")

        # 处理APP2
        # 填充0xFF
        app2.fill_bytes(fill=0xFF, end=None, alignment=128)
        # 写入包长字节到偏移0x08
        app2.write_length_bytes(offset=0x08)

        # 从0x0E开始计算CRC写入偏移0x04
        app2.crc32_update_revtab(offset=0x04, start=0x0E)
        # 更新文件供最后组包用
        app2.update()
        # 加密包, 从0x10地址开始
        app2.aes_ecb_encryptyion('5A435A66755436363669526467504E48', 0x10)
        # 从0x04开始计算CRC写入偏移0x00
        app2.crc32_update_revtab(offset=0x00, start=0x04)
        # 保存正式升级文件
        app2.save(f"{tmp_path}/Camel_03_KF13A017_{key}_APP2_V{ver2.hex()}.bin")

        # 还原文件
        app2.reset()
        # 修改版本号为0xFF
        app2.content[0x0E] = 0xFF
        # 从0x0E开始计算CRC写入偏移0x04
        app2.crc32_update_revtab(offset=0x04, start=0x0E)
        # 加密包, 从0x10地址开始
        app2.aes_ecb_encryptyion('5A435A66755436363669526467504E48', 0x10)
        # 从0x04开始计算CRC写入偏移0x00
        app2.crc32_update_revtab(offset=0x00, start=0x04)
        # 保存FF升级文件
        app2.save(f"{tmp_path}/Camel_03_KF13A017_{key}_APP2_V{ver2_FF.hex().upper()}.bin")

        # 烧录文件
        app1.reset()
        app2.reset()
        combine = boot + app1 + app2
        combine.save(f"{tmp_path}/Camel_03_KF13A017_{key}_V{ver1.hex()}-V{ver2.hex()}.bin")
        combine.bin2hex(f"{tmp_path}/Camel_03_KF13A017_{key}_V{ver1.hex()}-V{ver2.hex()}.hex")

    shutil.make_archive(f'./project/camel/output/Camel_03_KF13A017_Merged_'
                        f'V{app1_ver_list[0]}V{app1_ver_list[1]}V{app1_ver_list[2]}V{app1_ver_list[3]}-'
                        f'V{app2_ver_list[0]}V{app2_ver_list[1]}V{app2_ver_list[2]}V{app2_ver_list[3]}_'
                        f'{time.strftime("%Y_%m_%d_%H_%M_%S",time.localtime())}', 'zip', './temp')
