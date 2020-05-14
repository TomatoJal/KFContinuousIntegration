# -*- coding: UTF-8 -*-
from common.paraHandle import Parameter
from function.IARHandle.IARHandle import EWW
import os
import yaml


class ContinueIntegration:
    def __init__(self):
        self.__parameters_get()  # 参数获取
        self.__search_project()  # 文件夹寻找
        self.__prj_config_get()  # 获取项目配置
        self.__iar_info_get()    # IAR配置信息

    def __parameters_get(self):
        self.parameters = Parameter()

    def __search_project(self):
        self.prj_script_dir = r'./project/' + self.parameters.cmd_para['project']
        if not os.path.exists(self.prj_script_dir):
            self.parameters.parser.error(f"Not found project script dir: '{self.prj_script_dir}'")

    def __prj_config_get(self):
        with open(rf'{self.prj_script_dir}\config.yaml', encoding="utf-8") as f:
            c = yaml.load(f, Loader=yaml.FullLoader)
        self.prj_config = c['config']

    def __iar_info_get(self):
        self.iar = EWW(self.prj_config['eww_path'])
        pass



if __name__ == "__main__":
    ci = ContinueIntegration()
    pass