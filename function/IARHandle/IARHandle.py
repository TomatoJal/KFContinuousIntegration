# -*- coding: UTF-8 -*-
from lxml import etree
from collections import namedtuple
from common.logHandle import *
import subprocess
import os


def icf_file_analysis(file: str) -> list:
    try:
        start, end = 0, 0
        file = open(file, encoding='GBK', errors='ignore')
        for line in file.readlines():
            if 'define' in line and 'symbol' in line and '=' in line:
                line = [i for i in line.split(' ') if i != '']
                s = line.index('=')
                var = ''
                varName = line[s-1]
                for i in range(s+1, len(line)):
                    line[i] = line[i].split('//')[0]
                    var += line[i].replace(';', '').replace('\n', '')
                    if ';' in line[i]:
                        break

                    var = eval(var)
                    locals()[varName] = var
                if varName in ['__ICFEDIT_region_ROM_start__', 'FLASH_START', 'ROM_start__']:
                    start = var
                elif varName in ['__ICFEDIT_region_ROM_end__', 'FLASH_END', 'ROM_end__']:
                    end = var
        return [start, end]
    except:
        pass


class _Batch:
    def __init__(self):
        self.ewp = None
        self.batch = None


class _EWPConfiguration:
    def __init__(self):
        self.name = None
        # self.ewp = None
        self.ExePath = None
        self.CCIncludePath2 = None
        self.CCDefines = None
        self.IlinkIcfFile = None
        self.range = None


class EWP:
    def __init__(self, ewp: str):
        if ewp.endswith('.ewp') is False:
            raise TypeError("Except a .ewp file")

        self.PROJ_DIR = '\\'.join(ewp.split('\\')[:-1])

        self.__ewp_parse = etree.parse(ewp, etree.HTMLParser())

        self.ewp_path = ewp.replace('$PROJ_DIR$', self.PROJ_DIR)

        # name
        self.name = ewp.split('\\')[-1][:-4]

        # group file analysis
        self.group = [f.replace('$PROJ_DIR$', self.PROJ_DIR) for f in self.__ewp_parse.xpath('//file/name/text()')]

        # configuration analysis
        self._configuration_analysis()

    def _configuration_analysis(self):
        self.configuration = {}
        for configuration in self.__ewp_parse.xpath('//project/configuration'):
            name = configuration.xpath('./name/text()')[0]
            self.configuration[name] = _EWPConfiguration()
            # self.configuration[name].ewp = 'E:\\OnePiece\\Project\\0007.KFM\\Cetus_02_KF13A009M1\\IAR\\app1.ewp'
            self.configuration[name].name = name
            self.configuration[name].ExePath = self.PROJ_DIR + '\\' + configuration.xpath(
                './settings/data/option[name="ExePath"]/state/text()')[0] + '\\' + f'{self.name}.bin'
            self.configuration[name].CCIncludePath2 = [f.replace('$PROJ_DIR$', self.PROJ_DIR) for f in
                                                       configuration.xpath(
                                                           './settings/data/option[name="CCIncludePath2"]/state/text()')]
            self.configuration[name].CCDefines = [d for d in configuration.xpath(
                './settings/data/option[name="CCDefines"]/state/text()')]
            self.configuration[name].IlinkIcfFile = [f.replace('$PROJ_DIR$', self.PROJ_DIR) for f in
                                                     configuration.xpath(
                                                         './settings/data/option[name="IlinkIcfFile"]/state/text()')][0]
            self.configuration[name].range = icf_file_analysis(self.configuration[name].IlinkIcfFile)

class EWW:
    def __init__(self, eww: str):

        if eww.endswith('.eww') is False:
            raise TypeError("Except a .eww file")

        self.WS_DIR = '\\'.join(eww.split('\\')[:-1])  # eww路径

        self.project = {}  # ewp
        self.batchBuild = {}  # 工程对应链接

        self.__eww_parse = etree.parse(eww, etree.HTMLParser())  # eww文件

        self._project_analysis()   # 解析ewp工程

        self._batchBuild_analysisi()

    def _project_analysis(self):
        # 获取所有ewp文件
        for ewp in self.__eww_parse.xpath('//workspace/project/path/text()'):
            self.project[ewp.split('\\')[-1][:-4]] = ewp.replace('$WS_DIR$', self.WS_DIR)

    def _batchBuild_analysisi(self):
        try:
            prj_member = [p for p in self.__eww_parse.xpath('//workspace/batchbuild/batchdefinition')[0].xpath(
                './member/project/text()')]
            batchDefinition_member_namedtuple = namedtuple('batchDefinition_member', ' '.join(prj_member))
            for name in self.__eww_parse.xpath('//workspace/batchbuild/batchdefinition/name/text()'):
                configuration = self.__eww_parse.xpath(
                    f'//workspace/batchbuild/batchdefinition[name="{name}"]/member/configuration/text()')
                self.batchBuild[name] = batchDefinition_member_namedtuple(*configuration)
        except:
            pass

class IAR:
    def __init__(self, eww, IarBuild):
        self.IarBuild = IarBuild
        self.eww = EWW(eww)
        self.ewp = {}
        for key in self.eww.project.keys():
            self.ewp[key] = EWP(self.eww.project[key])

    def print_info(self):
        mat = "{:10}--\t{}"
        batch_mat = "{:20}--\t" + "{:10}" * len(self.ewp)
        info(mat.format("eww Path", self.eww.WS_DIR))
        info(mat.format("All ewp", ""))
        for value in self.eww.project.values():
            info(mat.format("", value))

        info(batch_mat.format("batchDefinition", *self.ewp.keys()))
        for key in self.eww.batchBuild.keys():
            info(batch_mat.format(key, *self.eww.batchBuild[key]))

    def build(self, configuration, action='make', log_level='info', varfile=None, output=None):
        """
        Usage: iarbuild
                    <projectfile> [-clean | -build | -make | -cstat_analyze | -cstat_clean]
                    <config> [-log errors|warnings|info|all] [-parallel <number>] [-varfile <argvarfile>]
        """
        if configuration not in self.eww.batchBuild.keys():
            error("Known configuration")
            return

        if action not in ['clean', 'build', 'make', 'cstat_analyze', 'cstat_clean']:
            error("Known action")
            return

        if log_level not in ['errors', 'warnings', 'info', 'all']:
            error("Known log level")
            return

        member = {}
        info(f"Start Build {configuration}")
        for ewp in self.eww.batchBuild[configuration]._fields:
            config = self.eww.batchBuild[configuration].__getattribute__(ewp)
            command = f"\"{self.IarBuild}\" \"{self.ewp[ewp].ewp_path}\" -{action} {config} -log {log_level}"
            member[config] = self.ewp[ewp].configuration[config]
            if output is not None:
                file = open(f"{output}/{ewp}.txt", 'w')
            info("{:10}--\t{}".format("Start Build", command))
            # 编译抓取log
            p = subprocess.Popen(command, stdout=subprocess.PIPE)
            result = p.wait()

            for line in p.stdout.readlines():
                msg = line.decode("gbk", "ignore")
                info(msg)
                if output is not None:
                    file.write(msg)
            if output is not None:
                file.close()
                info(f"Log write to file {output}\\{ewp}.txt")

            if result == 0:
                info(f"Build {config} Successful !")
            else:
                info(f"Build {config} Failed !")
                return None

        info(f"Build {configuration} Successful !")
        return member





if __name__ == "__main__":
    iar = IAR(r'E:\OnePiece\Project\0007.KFM\Cetus_02_KF13A009M1\IAR\PRJ.eww', r'D:\Work\IAR\common\bin\IarBuild.exe')
    iar.print_info()
    print(iar.build('Debug_sp'))
    # iar = IAR(r'E:\OnePiece\Project\0007.KFM\KFMFP-01-KF92P005\software\ewarm\ht6x3x\KFM.eww')
    # print(iar.__dict__)