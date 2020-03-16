# -*- coding: UTF-8 -*-
import os
from lxml import etree
from common import *
from collections import namedtuple


ewp_prj_namedtuple = namedtuple('ewp_prj', 'project exe_path')
ewp_namedtuple = namedtuple('ewp', 'path ewp_prj')


class IARComplier:
    def __init__(self, eww, IarBuild):
        """
        解析IAR配置文件
        :param eww: 项目文件
        :param IarBuild: 编译命令路径
        """
        self.IarBuild = f"\"{IarBuild}\\common\\bin\\IarBuild.exe\""

        self.__eww = eww
        self.ewp = {}
        self.__ws_dir = '\\'.join(self.__eww.split('\\')[:-1])

        # 解析eww
        c_file = etree.parse(self.__eww, etree.HTMLParser())
        for project in c_file.xpath('//workspace/project'):
            ewp_path = project.xpath('./path')[0].text
            self.ewp[ewp_path.split('\\')[-1].split('.')[0]] = ewp_namedtuple('\\'.join(ewp_path.split('\\')[:-1]),
                                                                              [])

        # 解析ewp
        for key in self.ewp.keys():
            c_file = etree.parse(f"{self.ewp[key].path.replace('$WS_DIR$', self.__ws_dir)}\\{key}.ewp",
                                 etree.HTMLParser())
            for configuration in c_file.xpath('//project/configuration'):
                self.ewp[key].ewp_prj.append(ewp_prj_namedtuple(configuration.xpath('./name')[0].text,
                                                                configuration.xpath('./settings')[0].xpath('./data')[
                                                                    0].xpath('./option')[0].xpath('./state')[0].text))

    def clean(self, ewp, log_level='info'):
        """
        :param ewp: 待执行ewp
        :param log_level:
                None        -   No log
                'errors'    -   Display build error messages.
                'warnings'  -   Display build warning and error messages.
                'info'      -   Display build warning and error messages, and messages
                                issued by the #pragma message preprocessor directive.
                'all'       -   Display all messages generated from the build,
                                for example compiler sign-on information and the
                                full command line.
        :return:
        """
        info(self.IarBuild)

    def build(self, need_log=True):
        info("Start build~~~~")
        self.clean()
        if need_log is True:
            text = os.popen(self.command.replace('commond', 'build') + " -log info")
        else:
            text = os.popen(self.command.replace('commond', 'build'))

        content = text.read()
        info(content)

        if content.find("ERROR, Command failed") != -1:
            error("Build Failed!")
            return -1
        else:
            info("Build Succeed!")
            return 0

