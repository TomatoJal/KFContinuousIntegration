# -*- coding: UTF-8 -*-
from common import *
import os


@tag('Camel')
def pack(config):
    """
    pack function for KFMFP_01_KF92P005
    :param config:
    :return: None
    """

    for key in config.keys():
        # 创建文件夹
        ver1 = config[key][1].content[0x0E: 0x10]
        ver1.reverse()
        ver1 = ver1.hex()
        ver2 = config[key][2].content[0x0E: 0x10]
        ver2.reverse()
        ver2 = ver2.hex()
        save_path = f'{pack.tmp_path}/{key}_V{ver1}_v{ver2}'

        os.makedirs(save_path)
        boot = config[key][0]
        app1 = config[key][1]
        app2 = config[key][2]
        for app in (app1, app2):
            # 获取版本号
            ver = app.content[0x0E: 0x10]
            ver.reverse()
            ver = ver.hex()
            # 填充0xFF
            app.fill_bytes(fill=0xFF, end=None, alignment=128)
            # 写入包长字节到偏移0x08
            app.write_length_bytes(offset=0x08)

            # 从0x0E开始计算CRC写入偏移0x04
            app.crc32_update_revtab(offset=0x04, start=0x0E)
            # 更新文件供最后组包用
            app.update()
            # 加密包, 从0x10地址开始
            app.aes_ecb_encryptyion('5A435A66755436363669526467504E48', 0x10)
            # 从0x04开始计算CRC写入偏移0x00
            app.crc32_update_revtab(offset=0x00, start=0x04)
            # 保存正式升级文件
            app.save(f"{save_path}/{app.name}_V{ver}_Upgrade.bin")

            # 还原文件
            app.reset()

            # 修改版本号为0xFF
            app.content[0x0E] = 0xFF
            # 更新版本号
            ver = app.content[0x0E: 0x10]
            ver.reverse()
            ver = ver.hex()
            # 从0x0E开始计算CRC写入偏移0x04
            app.crc32_update_revtab(offset=0x04, start=0x0E)
            # 加密包, 从0x10地址开始
            app.aes_ecb_encryptyion('5A435A66755436363669526467504E48', 0x10)
            # 从0x04开始计算CRC写入偏移0x00
            app.crc32_update_revtab(offset=0x00, start=0x04)
            # 保存FF升级文件
            # app1.save(f"{save_path}/Camel_03_KF13A017_{key}_APP1_V{ver1_FF.hex().upper()}.bin")
            app.save(f"{save_path}/{app.name}_V{ver}_Upgrade.bin")

        # 烧录文件
        app1.reset()
        app2.reset()
        combine = boot + app1 + app2
        combine.save(f"{save_path}/{pack.tag[0]}_V{ver1}-V{ver2}.bin")
        combine.bin2hex(f"{save_path}/{pack.tag[0]}_V{ver1}-V{ver2}.hex")

        pack.release_ver = f"V{ver1}-V{ver2}"
