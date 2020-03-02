# -*- coding: UTF-8 -*-
import argparse
from common import *

class Run(object):

    def __init__(self, args):
        self.args = args
        self.testCaseStatus = dict()
        self.main()


    # def searchAndRunTestCase(self):
    #     """
    #     根据 tag 和 untag 提取用例并执行
    #     :return:
    #     """
    #     # 将特殊 tag 添加到集合中
    #     self.args.tag = addSpecialTag(self.args.tag.split(","))
    #
    #     # 遍历模块下所有以".py"结尾的文件
    #     testcasedir = "projects" + os.sep + self.args.project.lower() + os.sep + self.args.feature.lower()
    #     if not os.path.exists(testcasedir):
    #         parser.error(f"Not found TestCaseDir: '{testcasedir}'")
    #         exit(-1)
    #
    #
    #     # 检查是否存在项目级的setup.py文件 (用于项目初始化操作)
    #     result = setupTearDown(project=self.args.project.lower(), feature="", isSetup=True)
    #     if result != 0:
    #         return
    #
    #     # 检查是否存在模块级的setup.py文件 (用于模块初始化操作)
    #     result = setupTearDown(project=self.args.project.lower(), feature=self.args.feature.lower(), isSetup=True)
    #     if result != 0:
    #         return
    #
    #     info("-------------------------- Test Start --------------------------")
    #     testResultList = list()
    #     for root, dirs, files in os.walk(testcasedir):
    #         for f in files:
    #             if f.endswith(".py") and f not in ['var.py', 'comm.py', 'setup.py', 'teardown.py']:
    #                 result = isContainTags(os.path.join(root, f), args.tag, args.untag)
    #                 if result[0]:
    #                     testResult = execTestcase(result[1])
    #                     if testResult is not None:
    #                         self.testCaseStatus[testResult[0]] = testResult[1]
    #                         if testResult[1] == 0:
    #                             content = f'{testResult[0].__doc__.strip()} *** succeeded! ***'
    #                             info(content)
    #                         else:
    #                             content = f'{testResult[0].__doc__.strip()} *** failed! ***'
    #                             error(content)
    #                             # 首次执行失败的也记录到'result.txt', 以备查看
    #                             writeTestResultToFile(content)
    #                         testResultList.append(testResult)
    #
    #
    #     # 检查是否存在模块级的teardown.py文件 (用于模块恢复设置操作)
    #     result = setupTearDown(project=self.args.project.lower(), feature=self.args.feature.lower(), isSetup=False)
    #     if result != 0:
    #         return
    #
    #     # 检查是否存在项目级的teardown.py文件 (用于项目恢复设置操作)
    #     result = setupTearDown(project=self.args.project.lower(), feature="", isSetup=False)
    #     if result != 0:
    #         return
    #
    #     info('')
    #     info("-------------------------- Test Result --------------------------")
    #     for testResult in testResultList:
    #         if testResult[1] == 0:
    #             info(f'{testResult[0].__doc__.strip()} *** succeeded! ***')
    #         else:
    #             error(f'{testResult[0].__doc__.strip()} *** failed! ***')
    #     info('');info('')
    #
    #
    # def reRunFailedTestCases(self):
    #     """
    #     将失败的用例重新执行一次
    #     :param args:
    #     :return:
    #     """
    #     filename = os.path.abspath(os.path.join("logs", kfLog.datetime, 'result.txt'))
    #     try:
    #         with open(filename, 'r') as fp:
    #             content = fp.read()
    #     except FileNotFoundError as ex:
    #         error(ex)
    #         exc_type, exc_value, exc_traceback_obj = sys.exc_info()
    #         error("".join(traceback.format_exception(exc_type, exc_value, exc_traceback_obj)))
    #         return
    #
    #     # 修改 tag 后, 重新执行
    #     arglist = list(set(re.findall('TestCase:\s*(.*)\.py.*\*\*\* failed! \*\*\*', content)))
    #     if len(arglist) > 0:
    #         for index, item in enumerate(arglist):
    #             # 查找同一子模块中是否存在以'000'命名的特殊脚本 (要求: 脚本文件名最后一段必须是三个数值)
    #             initialFile = re.sub(r'_(\d{3})', '_000', item)
    #             if initialFile not in arglist:
    #                 arglist.insert(index, initialFile)
    #
    #         self.args.tag = ",".join(arglist)
    #         self.args.rerun = 0
    #         self.searchAndRunTestCase()
    #
    #
    # def main(self):
    #
    #     # 查找用例并执行
    #     self.searchAndRunTestCase()
    #
    #     # 执行失败的用例
    #     # for i in range(args.rerun):
    #     if int(args.rerun) != 0:
    #         self.reRunFailedTestCases()
    #
    #     content = "-------------------------- Final Result --------------------------"
    #     info(''); info(content); writeTestResultToFile(content)
    #     ok = nok = 0
    #     for func, status in self.testCaseStatus.items():
    #         if status == 0:
    #             content = f'{func.__doc__.strip()} *** succeeded! ***'
    #             info(content)
    #             ok += 1
    #             writeTestResultToFile(content)
    #         else:
    #             content = f'{func.__doc__.strip()} *** failed! ***'
    #             error(content)
    #             nok += 1
    #             writeTestResultToFile(content)
    #
    #     # 统计结果
    #     content = "-------------------------- Statistic --------------------------"
    #     info(content)
    #     writeTestResultToFile(content)
    #     content = f'Total Testcase: {ok+nok}; Succeed: {ok}; Failed: {nok}\n'
    #     info(content)
    #     writeTestResultToFile(content)
    #
    #
    #     # 将Log转化成Html格式
    #     logToHtml()



# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description="Package tool")
#
#     # 用例选择相关参数
#     parser.add_argument("-p", "--project", type=str, help="project name: such as amber51, camel...")
#
#     # 解析数据
#     args = parser.parse_args()
#
#     # 更新项目名称
#     if args.project is None:
#         parser.error("'project' argument is needed!")
#
#     # 执行
#     Run(args)

if __name__ == "__main__":
    # 打开文件
    file = Bin(r'C:\Users\tomat\Desktop\Camel\test\app1.bin')
    # 填充0xFF
    file.fill_bytes()
    # 写入包长字节到偏移0x08
    file.write_length_bytes(offset=0x08)
    # 从0x0E开始计算CRC写入偏移0x04
    file.crc32_update_revtab(offset=0x04, start=0x0E)
    # 加密包
    file.aes_ecb_encryptyion('5A435A66755436363669526467504E48', 0x10)
    # 从0x04开始计算CRC写入偏移0x00
    file.crc32_update_revtab(offset=0x00, start=0x04)
    # 保存
    file.save(r"C:\Users\tomat\Desktop\1.bin")

