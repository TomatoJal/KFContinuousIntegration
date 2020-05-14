# -*- coding: UTF-8 -*-
import argparse
import yaml
from common.logHandle import *


class Parameter:
    def __init__(self):
        self._cmd_para()
        self._env_para()

    def _cmd_para(self):
        """
        处理传入参数
        :return: Null
        """
        self.parser = argparse.ArgumentParser(description="Continue Integration")
        self.parser.add_argument("project", help="project name: such as amber51, camel...")
        #
        #
        # self.parser.add_argument("-c", "--commit", help="checkout to commit/branch/tag")
        # self.parser.add_argument("-b", "--build", action="store_true", help="need build?")
        # self.parser.add_argument("-p", "--pack", nargs='*', help="need pack, can add save path")
        # self.parser.add_argument("--doxygen", action="store_true", help="run doxygen?")
        # self.parser.add_argument("--PCLint", action="store_true", help="run PCLint?")
        args = self.parser.parse_args()
        # 转换为dict
        self.cmd_para = vars(args)
        # self.cmd_para = args

    def _env_para(self):
        """
        处理环境参数
        :return: Null
        """
        # 读取环境配置文件
        with open(r'config\environment.yaml', encoding="utf-8") as f:
            c = yaml.load(f, Loader=yaml.FullLoader)
            self.env_para = c['environment']



if __name__ == "__main__":
    test = Parameter()


