# -*- coding: UTF-8 -*-
import argparse
from compiler import *
from pack import *
import yaml
import os
import shutil


class Project:

    def __init__(self):
        self.basic_info = {}
        self.system_info = {}
        self.project_info = {}
        self.project_info.update({'bin': {}})
        self.project = {}
        self.pack_func = None

    def search_project(self):
        prj_dir = r'./project/' + self.basic_info['project_name']
        if not os.path.exists(prj_dir):
            parser.error(f"Not found TestCaseDir: '{prj_dir}'")
            exit(-1)
        self.basic_info['project_path'] = prj_dir

        if self.basic_info['pack'] is True:
            if not os.path.exists(f"{self.basic_info['project_path']}/pack.py"):
                error(f"Not found the script: pack.py")
                exit(-1)
            obj = __import__(f"project.{self.basic_info['project_name']}.pack", fromlist=['all'])
            self.pack_func = obj.pack

    def main(self):
        # 搜寻项目路径
        self.search_project()

        # 获取项目配置, 并编译
        with open(self.basic_info['project_path'] + r'\config.yaml', encoding="utf-8") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            if 'IAR' in config['config']['compiler']:
                self.project_info['IAR'] = config['IAR']
                for part in self.project_info['IAR']['compile_prj']:
                    self.project[part] = {}
                    self.project_info['bin'][part] = {}
                    for prj in self.project_info['IAR']['compile_prj'][part]:
                        self.project[part][prj] = IARComplier(
                            self.system_info['IAR_path'][self.project_info['IAR']['IAR_ver']],
                            self.project_info['IAR']['IAR_prj_path'], part, prj)
                        if self.basic_info['build'] is True:
                            if self.project[part][prj].build() == -1:
                                exit(-1)

                        self.project_info['bin'][part][self.project[part][prj].project_name] = Bin(
                            self.project[part][prj].exe_file, self.project_info['IAR']['offset'][part])
            # GCC
            else:
                pass


        # 进行打包
        if self.basic_info['pack'] is True:
            self.pack_func(self.project_info)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Package tool")

    # 项目选择相关参数
    parser.add_argument("project", help="project name: such as amber51, camel...")
    parser.add_argument("-b", "--build", action="store_true", help="need build?")
    parser.add_argument("-p", "--pack", action="store_true", help="need pack?")
    # 解析数据
    args = parser.parse_args()

    # 更新项目名称
    if args.project is None:
        parser.error("'project' argument is needed!")

    # 清理临时文件夹
    if os.path.exists('./temp') is True:
        shutil.rmtree('./temp')
    os.makedirs('./temp')

    # 读取全局配置文集
    with open(r'config\environment.yaml', encoding="utf-8") as f:
        system_info = yaml.load(f, Loader=yaml.FullLoader)['environment']

    # 创建项目对象
    project = Project()
    project.basic_info['project_name'] = args.project
    project.basic_info['build'] = args.build
    project.basic_info['pack'] = args.pack
    project.system_info = system_info

    info(f"Start project {project.basic_info['project_name']}")

    try:
        project.main()
    finally:
        info('End~~~~~~~~~~~~~~')





