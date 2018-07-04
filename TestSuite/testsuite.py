#!/usr/bin/env python3
# coding:utf-8

import os
import time
import unittest
from Common.HTMLTestRunner import HTMLTestRunner
from Common.mylog import MyLog

mylog = MyLog().mylog()

current_path = os.path.dirname(os.path.realpath(__file__))  # 脚本当前路径
case_dir = os.path.join(os.path.dirname(current_path), 'TestCase')  # TestCase文件夹路径
report_dir = os.path.join(os.path.dirname(current_path), 'Report')  # 测试报告的文件夹路径


class TestSuite:
    """测试用例套件"""

    def __init__(self):
        """
        初始化读取待执行的测试用例
        """
        self.case_list = []
        self.suite_list = []

        caselist_path = os.path.join(case_dir, 'caselist.txt')
        mylog.info('Get test case list from txt:{}'.format(os.path.basename(caselist_path)))
        with open(caselist_path) as f:
            for line in f.readlines():
                if line != '\n' and not line.startswith('#'):  # 去除本行是空行或者注释掉的用例
                    self.case_list.append(line.strip())

    def suite(self):
        """
        根据待执行测试用例名称装载测试套件
        :return: 测试用例套件
        """
        mylog.info('Set test suite.')
        for case in self.case_list:
            case_name = case.split('/')[1]  # 获得测试用例名称
            discover = unittest.defaultTestLoader.discover(case_dir, pattern=case_name, top_level_dir=None)
            self.suite_list.append(discover)
        suite = unittest.TestSuite(self.suite_list)  # 装载测试用例
        return suite

    def run(self):
        """
        执行测试用例，并写入测试报告
        :return: 测试测试报告
        """
        mylog.info('Run test case.')
        suite = self.suite()
        now = time.strftime('%Y-%m-%d %H_%M_%S')
        report_path = os.path.join(report_dir, 'TestResult ' + now + '.html')
        fp = open(report_path, 'wb')
        runner = HTMLTestRunner(stream=fp, title='接口自动化测试报告', description='环境：测试环境')
        runner.run(suite)  # 执行所有测试用例
        mylog.info('Generate test report:{}'.format(os.path.basename(report_path)))
        return report_path


if __name__ == '__main__':
    testsuite = TestSuite()
    testsuite.run()
