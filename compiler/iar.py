# -*- coding: UTF-8 -*-
import os
from lxml import etree
from common import *


class IARComplier:
    def __init__(self, IarBuild, prj_path, ewp, project):
        self.__IarBuild = IarBuild
        self.__ewp = (prj_path + '/' + ewp).replace('\\', '/') + '.ewp'
        self.ewp = ewp
        self.project_name = project
        self.__IarBuild = self.__IarBuild.replace('\\', '/')
        # 此处注意调用exe左右加‘“’,否则命令行只会识别到空格
        self.command = rf'"{self.__IarBuild}/common/bin/IarBuild.exe" {self.__ewp} -commond {self.project_name}'

        # 获取exe位置
        self.exe_file = None
        c_file = etree.parse(self.__ewp, etree.HTMLParser())
        for configuration in c_file.xpath('//project/configuration'):
            for name in configuration.xpath('./name'):
                if self.project_name == name.text:
                    self.exe_file = (prj_path + '/' + configuration.xpath('./settings')[0].xpath('./data/option/state')[0].text).replace('\\', '/') + '/' + self.ewp + '.bin'
                    break

    def clean(self, need_log=True):
        info("Start clean~~~~")
        if need_log is True:
            info(self.command.replace('commond', 'clean') + " -log all")
            text = os.popen(self.command.replace('commond', 'clean') + " -log all")
        else:
            info(self.command.replace('commond', 'clean'))
            text = os.popen(self.command.replace('commond', 'clean'))
        info(text.read())
        info("Clean end~~~~")

    def build(self, need_log=True):
        info("Start build~~~~")
        self.clean()
        if need_log is True:
            text = os.popen(self.command.replace('commond', 'build') + " -log all")
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

