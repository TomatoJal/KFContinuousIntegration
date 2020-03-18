# -*- coding: UTF-8 -*-
from common import *
import os
import shutil
import time

@tag('KFMFP_01_KF92P005')
def save(release_path):
    """
    save function for KFMFP_01_KF92P005
    :param release_path: 输出路径
    :return:
    """
    shutil.make_archive(f'{release_path}\\{save.tag[0]}_{save.release_ver}'
                        f'({time.strftime("%Y_%m_%d_%H_%M", time.localtime())})',
                        'zip', save.tmp_path)
