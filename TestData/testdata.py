#!/usr/bin/env python3
# coding:utf-8

import os
from Common.myexcel import MyExcel
from Common.myxml import MyXml
from Common.mylog import MyLog
from Common.mysql import MySql


mylog = MyLog().mylog()
# 注意：这里不要使用os.getcwd()，模块被引用后，获取的是外层调用的脚本路径
current_path = os.path.dirname(os.path.realpath(__file__))  # 脚本所在当前路径
case_data_path = os.path.join(current_path, 'CaseData')  # 测试数据所在路径
case_database_path = os.path.join(current_path, 'CaseDatabase')  # 测试数据库xml所在路径


def read_data(excel_name, sheet_name):
    """
    读取excel中测试用例的数据
    :param excel_name: 测试用例excel名称
    :param sheet_name: excel中sheet页名称
    :return: 测试用例相关数据
    """
    excel_path = os.path.join(case_data_path, excel_name)
    mylog.info('Read test data from excel:{}'.format(excel_name))
    myexcel = MyExcel(excel_path)
    book = myexcel.read_book()  # 获取book形式数据
    sheet = book.sheet_by_name(sheet_name)  # 获取sheet页数据
    data = sheet.get_array()  # 获取二维数组形式数据
    return data


def generate_data(xml_name='CaseDatabase.xml'):
    """
    初始化数据库数据
    :param xml_name: 数据库xml配置文件名称
    :return:
    """
    xml_path = os.path.join(case_database_path, xml_name)
    mylog.info('Init database from xml:{}'.format(xml_name))
    myxml = MyXml(xml_path)
    page = myxml.read_xml()  # 得到xml的根节点
    excel_list = page.findall('excel')  # 获取所有excel节点
    for excel in excel_list:
        mysql = MySql()
        mysql.connect()
        excel_name = excel.get('name')  # 获得excel名称
        sheet_list = excel.findall('sheet')  # 获得当前excel的sheet节点
        for sheet in sheet_list:
            sheet_name = sheet.get('name')  # 得到sheet名称
            data = read_data(excel_name, sheet_name)  # 获得当前sheet页的数据
            case_field = data[0]  # 获得用例字段列表，即excel第一行
            for case_data in data[1:]:  # 用例的数据实际是从excel的第二行开始的
                generate_data_num = case_field.index('generate_data')  # 用例是否需要生成数据库数据的字段索引
                is_generate_data = case_data[generate_data_num]  # 用例是否需要生成数据库数据的字段数据:'True'/'False'
                if is_generate_data == 'True':
                    database_list = sheet.findall('database')  # 得到sheet下所有的database节点
                    for database in database_list:
                        database_name = database.get('name')  # 获得数据库名称
                        table_list = database.findall('table')  # 得到database下所有的table节点
                        for table in table_list:
                            table_name = table.get('name')  # 获得数据表名称
                            field_list = table.findall('field')  # 得到table下所有field节点
                            fields = ''  # 定义写入数据表的字段
                            values = ''  # 定义写入数据表的数据
                            for field in field_list:
                                fields = fields + field.text + ','  # 数据表字段合成字符串，用','隔开
                                field_num = case_field.index(field.get('name'))  # 写入数据表的字段索引位置
                                values = values + str(case_data[field_num]) + ','  # 写入数据合成字符串，用','隔开
                            # sql语句格式化，fields和values在合成字符串时末尾保留了','，所以需要去掉
                            sql = 'INSERT {table_name}({fields}) VALUES({values})'\
                                .format(table_name=table_name, fields=fields.rstrip(','), values=values.rstrip(','))
                            mysql.execute(sql)  # 执行sql语句，初始化数据库
        mysql.close()  # 关闭数据库


def clear_data(xml_name='CaseDatabase.xml'):
    """
    清空数据库数据
    :param xml_name: 数据库xml配置文件名称
    :return:
    """
    xml_path = os.path.join(case_database_path, xml_name)  # 获取xml文件路径
    mylog.info('Clear database from xml:{}'.format(xml_name))
    myxml = MyXml(xml_path)
    page = myxml.read_xml()  # 得到xml的根节点
    clear = page.find('clear')  # 获取clear节点
    database_list = clear.findall('database')  # 得到sheet下所有的database节点
    for database in database_list:
        database_name = database.get('name')  # 获得数据库名称
        mysql = MySql()
        mysql.connect()
        table_list = database.findall('table')  # 得到database下所有的table节点
        for table in table_list:
            table_name = table.text  # 获得数据表名称
            sql = 'DELETE FROM {table_name}'.format(table_name=table_name)
            mysql.execute(sql)  # 执行sql语句，初始化数据库
            mysql.close()  # 关闭数据库


if __name__ == '__main__':
    clear_data('CaseDatabase.xml')
    generate_data('CaseDatabase.xml')
    testcase_data = read_data('getQiyiVipUserInfo.xlsx', '获取爱奇艺会员到期时间接口')
    print(testcase_data)
