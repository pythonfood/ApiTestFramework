#!/usr/bin/env python3
# coding:utf-8

import os
import pyexcel
from Common.mylog import MyLog

mylog = MyLog().mylog()


class MyExcel:
    """读取excel文件"""

    def __init__(self, excel_path):
        """
        初始化读取excel文件，获取book形式数据
        :param excel_path: excel文件
        """
        try:
            self.book = pyexcel.get_book(file_name=excel_path)
            mylog.info('Read exel:{}'.format(os.path.basename(excel_path)))
        except Exception:
            mylog.error('Read exel:{} faild !'.format(excel_path))

    def read_book(self):
        """
        读取book形式数据
        :return: book形式数据
        """
        return self.book


if __name__ == '__main__':
    myexcel = MyExcel(r'D:\PycharmProjects\TestFramework\TestData\CaseData\getQiyiVipUserInfo.xlsx')
    book = myexcel.read_book()
    print(book)



