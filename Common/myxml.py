#!/usr/bin/env python3
# coding:utf-8

from xml.etree import ElementTree
from Common.mylog import MyLog

mylog = MyLog().mylog()


class MyXml:
    """读取xml文件"""

    def __init__(self, xml_name):
        """
        初始化读取xml文件，获取根节点
        :param xml_name: xml文件
        """
        try:
            self.et = ElementTree.parse(xml_name)
            self.root = self.et.getroot()
        except Exception:
            mylog.error('Read {} faild!'.format(xml_name))

    def read_xml(self):
        """
        读取xml文件内容
        :return: xml根节点
        """
        return self.root


if __name__ == '__main__':
    myxml = MyXml(r'D:\PycharmProjects\TestFramework\TestData\CaseDatabase\CaseDatabase.xml')
    page = myxml.read_xml()
    excel_list = page.findall('excel')
    for excel in excel_list:
        excel_name = excel.get('name')
        print(excel_name)
