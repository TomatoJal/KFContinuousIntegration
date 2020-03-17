# -*- coding: UTF-8 -*-
import os
from lxml import etree
from common import *
from collections import namedtuple


ewp_namedtuple = namedtuple('ewp', 'path ewp_prj')


class IARComplier:
    """
    If you have a project file named test.ewp with a configuration named Debug,
    the following command can be used to build the project:

        <installation dir>\common\bin\IarBuild.exe test.ewp Debug

    Note: Run IarBuild.exe without parameters to get usage information.

    To rebuild the project, use the following command (extended with an option to log all compiler messages):

        <installation dir>\common\bin\IarBuild.exe test.ewp -build Debug -log all

    The rebuild command above corresponds to:

        <installation dir>\common\bin\IarBuild.exe test.ewp -clean Debug -log all
        <installation dir>\common\bin\IarBuild.exe test.ewp -make Debug -log all
    """
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
                                                                              {})

        # 解析ewp
        for key in self.ewp.keys():
            c_file = etree.parse(f"{self.ewp[key].path.replace('$WS_DIR$', self.__ws_dir)}\\{key}.ewp",
                                 etree.HTMLParser())
            for configuration in c_file.xpath('//project/configuration'):
                self.ewp[key].ewp_prj[configuration.xpath('./name')[0].text] = \
                configuration.xpath('./settings')[0].xpath('./data')[0].xpath('./option')[0].xpath('./state')[0].text

    def clean(self, ewp, project, log_level='info'):
        """
        :param ewp: 待执行ewp
        :param project: 待执行的project
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
        ewp = '\"' + '\\'.join([self.ewp[ewp].path.replace('$WS_DIR$', self.__ws_dir), ewp]) + '.ewp\"'
        if log_level is not None:
            command = f"{self.IarBuild} {ewp} -clean {project} -log {log_level}"
        else:
            command = f"{self.IarBuild} {ewp} -clean {project}"
        info(command)
        content = os.popen(command).read()
        info(content)
        if content.find("ERROR, Command failed") != -1:
            error(f"Clean {ewp} {project} Failed!")
            return -1
        else:
            info(f"Clean {ewp} {project} Succeed!")
            return 0

    def build(self, ewp, project, log_level='info'):
        """
        :param ewp: 待执行ewp
        :param project: 待执行的project
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
        ewp = '\"' + '\\'.join([self.ewp[ewp].path.replace('$WS_DIR$', self.__ws_dir), ewp]) + '.ewp\"'
        if log_level is not None:
            command = f"{self.IarBuild} {ewp} -build {project} -log {log_level}"
        else:
            command = f"{self.IarBuild} {ewp} -build {project}"
        info(command)
        content = os.popen(command).read()
        info(content)
        if content.find("ERROR, Command failed") != -1:
            error(f"Build {ewp} {project} Failed!")
            return -1
        else:
            info(f"Build {ewp} {project} Succeed!")
            return 0

