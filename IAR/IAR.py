# -*- coding: UTF-8 -*-
from lxml import etree
from collections import namedtuple


def icf_file_analysis(file: str) -> tuple:
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
            try:
                var = eval(var)
                locals()[varName] = var
            except:
                pass
            if varName in ['__ICFEDIT_region_ROM_start__', 'FLASH_START', 'ROM_start__']:
                start = var
            elif varName in ['__ICFEDIT_region_ROM_end__', 'FLASH_END', 'ROM_end__']:
                end = var
    return (start, end)


class EWPConfiguration:
    def __init__(self):
        self.name = None
        self.ExePath = None
        self.ObjPath = None
        self.ListPath = None
        self.CCIncludePath2 = None
        self.CCDefines = None
        self.IlinkIcfFile = None
        self.range = None


class EWP:
    def __init__(self, ewp: str):
        if ewp.endswith('.ewp') is False:
            raise TypeError("Except a .ewp file")
        self.PROJ_DIR = '\\'.join(ewp.split('\\')[:-1])
        self.__ewp = etree.parse(ewp, etree.HTMLParser())

        # name
        self.name = ewp.split('\\')[-1][:-4]

        # group file analysis
        self.__group_analysis()

        # configuration analysis
        self.__configuration_analysis()


    def __group_analysis(self):
        self.group = [f.replace('$PROJ_DIR$', self.PROJ_DIR) for f in self.__ewp.xpath('//file/name/text()')]

    def __configuration_analysis(self):
        self.configuration = {}
        for namex in self.__ewp.xpath('//configuration/name'):
            name = namex.text
            self.configuration[name] = EWPConfiguration()
            self.configuration[name].name = name
            configuration = namex.xpath('..')[0]
            self.configuration[name].ExePath = self.PROJ_DIR + '\\' + configuration.xpath(
                './settings/data/option[name="ExePath"]/state/text()')[0]
            self.configuration[name].ObjPath = self.PROJ_DIR + '\\' + configuration.xpath(
                './settings/data/option[name="ObjPath"]/state/text()')[0]
            self.configuration[name].ListPath = self.PROJ_DIR + '\\' + configuration.xpath(
                './settings/data/option[name="ListPath"]/state/text()')[0]
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
        self.WS_DIR = '\\'.join(eww.split('\\')[:-1])
        self.__eww = etree.parse(eww, etree.HTMLParser())
        self.__project_analysis()
        self.__batchBuild_analysisi()

    def __project_analysis(self):
        """ project """
        self.__ewp = []
        for project in self.__eww.xpath('//project/path'):
            self.__ewp.append(EWP(project.text.replace('$WS_DIR$', self.WS_DIR)))

    def __batchBuild_analysisi(self):
        """ batchBuild """
        self.batchBuild = {}
        # 构建命名结构
        batchDefinition_member_namedtuple = namedtuple('batchDefinition_member',
                                                       ' '.join([p for p in
                                                                 self.__eww.xpath('//batchbuild/batchdefinition')[
                                                                     0].xpath('./member/project/text()')]))
        for batchDefinition in self.__eww.xpath('//batchbuild/batchdefinition'):
            name = batchDefinition.xpath('./name')[0].text
            self.batchBuild[name] = batchDefinition_member_namedtuple(
                *[c for c in batchDefinition.xpath('./member/configuration/text()')])


# class IAR:
#
#
#     def _eww_analysis(self):
#         eww = etree.parse(self.__eww, etree.HTMLParser())
#         # 添加project





if __name__ == "__main__":
    iar = EWW(r'E:\OnePiece\Project\0007.KFM\Cetus05-KF_13A009M_IDIS\IAR\PRJ.eww')
    # print(iar.__dict__)