# -*- coding: UTF-8 -*-
import argparse
from compiler import *
from pack import *
import yaml
import os
import traceback
import sys
from common import *
import time


class Project:

    def __init__(self):
        self.basic_info = {
            'project_name': '',       # 项目名
            'prj_script_dir': '',     # 待运行脚本路径
            'build': False,  # 是否需要编译
            'pack': False,   # 是否需要打包
        }    # 基础信息, 取自输入参数
        self.environment_info = {}  # 环境信息, 取自environment.yaml为文件

        self.project_info = {}

        self.project = {}
        self.interface = {
            'pack': None,   # 打包接口
            'save': None,   # 存储接口
        }   # 后续操作接口

    def init_project(self):
        """
        初始化项目
        :return: None
        """
        if self.basic_info['pack'] is True:
            for i in ('pack', 'save'):
                if not os.path.exists(f"{self.basic_info['prj_script_dir']}/{i}.py"):
                    raise Exception(f"Not found the pack script: {i}.py.")
                obj = __import__(f"project.{self.basic_info['project_name']}.{i}", fromlist=['all'])
                self.interface[i] = obj.__getattribute__(f'{i}')

        with open(self.basic_info['prj_script_dir'] + r'\config.yaml', encoding="utf-8") as file:
            self.project_info = yaml.load(file, Loader=yaml.FullLoader)

    def build_project_with_iar(self):
        """
        IAR编译
        :param config: 从项目文件夹中获取的配置文件
        :return: None
        """
        # 获取IAR配置项
        info("Start analysis IAR")
        info(f"Use IAR version  -- {self.project_info['IAR']['IAR_ver']}")
        info(f"Project path     -- {self.project_info['IAR']['IAR_prj_path']}")
        info(f"IAR project      -- {self.project_info['IAR']['IAR_prj_name']}.eww")
        info("Offset: ")
        for key in self.project_info['IAR']['offset'].keys():
            info(f"\t\t{key} -- {hex(self.project_info['IAR']['offset'][key])[2:].rjust(8, '0').upper()}")
        info("Firmware:")
        for key in self.project_info['IAR']['firmware'].keys():
            info(f"\t\t{key} -- {self.project_info['IAR']['firmware'][key]}")

        iar = IARComplier(f"{self.project_info['IAR']['IAR_prj_path']}\\"
                          f"{self.project_info['IAR']['IAR_prj_name']}.eww",
                          self.environment_info['IAR_path'][self.project_info['IAR']['IAR_ver']])

        # 检查是否所有打包所需ewp文件都包含且能编译通过
        for prj in self.project_info['IAR']['firmware'].keys():
            for i in range(0, len(self.project_info['IAR']['firmware'][prj])):
                ewp = list(self.project_info['IAR']['offset'].keys())[i]
                if iar.build(ewp, self.project_info['IAR']['firmware'][prj][i]) == -1:
                    raise Exception(f"Build {ewp} Fail")

    def build_project_with_eclipse(self):
        """
        eclipse编译
        :return: None
        """
        # 获取eclipse配置项
        info("Start analysis eclipse")
        info(f"Use gcc version  -- {self.project_info['eclipse']['GCC_ver']}")
        info(f"Project path     -- {self.project_info['eclipse']['eclipse_prj_path']}")
        info(f"eclipse project  -- {self.project_info['eclipse']['eclipse_prj_name']}")
        gcc = GCCComplier(self.project_info['eclipse'],
                          self.environment_info['GCC_path'][self.project_info['eclipse']['GCC_ver']])

    def build_project(self):
        # 获取项目配置, 并编译
        info(f"Compile with -- {self.project_info['config']['compiler']}")
        if 'IAR' in self.project_info['config']['compiler']:
            info("Compile start with IAR")
            self.build_project_with_iar()

        # eclipse
        if 'eclipse' in self.project_info['config']['compiler']:
            info("Compile start with eclipse")
            self.build_project_with_eclipse()

    def pack_project(self):
        if 'IAR' not in self.project_info['config']['compiler']:
            raise Exception("Pack needs IAR, please config the compiler: -> IAR")
        # 获取bin文件
        iar = IARComplier(f"{self.project_info['IAR']['IAR_prj_path']}\\"
                          f"{self.project_info['IAR']['IAR_prj_name']}.eww",
                          self.environment_info['IAR_path'][self.project_info['IAR']['IAR_ver']])
        for key in self.project_info['IAR']['firmware'].keys():
            for i in range(0, len(self.project_info['IAR']['offset'])):
                ewp = list(self.project_info['IAR']['offset'].keys())[i]
                bin_path = f"{iar.ewp[ewp].path.replace('$WS_DIR$', self.project_info['IAR']['IAR_prj_path'])}\\" \
                           f"{iar.ewp[ewp].ewp_prj[self.project_info['IAR']['firmware'][key][i]]}\\" \
                           f"{ewp}.bin"
                self.project_info['IAR']['firmware'][key][i] = Bin(bin_path, self.project_info['IAR']['offset'][ewp],
                                                                   ewp)

        # 执行打包, 创建临时文件夹
        self.interface['pack'].tmp_path = f"./temp/{self.interface['pack'].tag[0]}_" \
                                          f"({time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime())})"
        os.makedirs(self.interface['pack'].tmp_path)
        self.interface['pack'](self.project_info['IAR']['firmware'])

        # 保存
        item_path = f"{self.basic_info['release_path']}\\{self.basic_info['project_name']}"
        if os.path.exists(item_path) is False:
            os.makedirs(item_path)
        if self.basic_info['sample'] is not None:
            self.interface['save'].tag = [self.basic_info['sample']]
            sample_path = f"{self.basic_info['release_path']}\\{self.basic_info['project_name']}\\" \
                          f"Sample_{self.basic_info['sample']}"
            if os.path.exists(sample_path) is False:
                os.makedirs(sample_path)
        else:
            sample_path = f"{self.basic_info['release_path']}\\{self.basic_info['project_name']}\\" \
                          f"{self.basic_info['project_name']}"
            if os.path.exists(sample_path) is False:
                os.makedirs(sample_path)
        self.interface['save'].tmp_path = self.interface['pack'].tmp_path
        self.interface['save'].release_ver = self.interface['pack'].release_ver
        self.interface['save'](sample_path)

    def main(self):
        # 初始化项目接口
        self.init_project()
        # 编译
        if self.basic_info['build'] is True:
            info("Start building project")
            self.build_project()

        # 进行打包
        if self.basic_info['pack'] is True:
            info("Start packing project")
            self.pack_project()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Package tool")

    # 项目选择相关参数
    parser.add_argument("project", help="project name: such as amber51, camel...")
    parser.add_argument("-b", "--build", action="store_true", help="need build?")
    parser.add_argument("-p", "--pack", action="store_true", help="need pack?")
    parser.add_argument("-s", "--sample", help="is a sample?")
    # 解析数据
    args = parser.parse_args()

    # 更新项目名称
    if args.project is None:
        parser.error("'project' argument is needed!")

    # 清理临时文件夹
    # if os.path.exists('./temp') is True:
    #     shutil.rmtree('./temp')
    # os.makedirs('./temp')

    # 创建项目对象, 构建基础信息
    project = Project()
    project.basic_info['project_name'] = args.project
    project.basic_info['build'] = args.build
    project.basic_info['pack'] = args.pack
    project.basic_info['sample'] = args.sample

    prj_script_dir = r'./project/' + project.basic_info['project_name']
    if not os.path.exists(prj_script_dir):
        parser.error(f"Not found TestCaseDir: '{prj_script_dir}'")
        exit(-1)
    project.basic_info['prj_script_dir'] = prj_script_dir

    # 读取全局配置文集
    with open(r'config\environment.yaml', encoding="utf-8") as f:
        c = yaml.load(f, Loader=yaml.FullLoader)
        project.environment_info = c['environment']
        project.basic_info['release_path'] = c['release_path']
    info('*' * 80)
    info('*' * 37 + 'STARTS' + '*' * 37)
    info('*' * 80)
    info(f"Project name       -- {project.basic_info['project_name']}")
    info(f"Project script dir -- {project.basic_info['prj_script_dir']}")
    info(f"Build              -- {project.basic_info['build']}")
    info(f"Pack               -- {project.basic_info['pack']}")

    try:
        project.main()

    except Exception as ex:
        error(f"** Meet exception ** :\n{ex}\n")
        exc_type, exc_value, exc_traceback_obj = sys.exc_info()
        error("".join(traceback.format_exception(exc_type, exc_value, exc_traceback_obj)))
        exit(-1)

    finally:
        info('*'*80)
        info('*'*38 + 'ENDS' + '*'*38)
        info('*'*80)






