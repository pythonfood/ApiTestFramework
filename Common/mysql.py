#!/usr/bin/env python3
# coding:utf-8

import pymysql
from Common.mylog import MyLog
from Config.readConfig import ReadConfig

mylog = MyLog().mylog()

readconfig = ReadConfig()  # 声明读取配置文件对象


class MySql:
    """数据库连接、执行sql、查询结果、关闭连接"""

    def __init__(self):
        """
        初始化读取数据库配置
        """
        self.host = readconfig.mysql('host')
        self.port = readconfig.mysql('port')
        self.username = readconfig.mysql('username')
        self.password = readconfig.mysql('password')
        self.database = readconfig.mysql('database')
        self.mysql_config = {
            'host': str(self.host),
            'user': self.username,
            'passwd': self.password,
            'port': int(self.port),
            'database': self.database
        }
        self.db = None  # 初始化数据库对象
        self.cursor = None  # 初始化游标对象

    def connect(self):
        """
        连接数据库
        """
        try:
            self.db = pymysql.connect(**self.mysql_config)
            self.cursor = self.db.cursor()
            mylog.info('Connect database:{}'.format(self.database))
        except ConnectionError:
            mylog.error('Connect database:{} faild!'.format(self.database))
            mylog.error(str(ConnectionError))

    def execute(self, sql):
        """
        执行sql语句
        :param sql: 需要执行的sql
        :return:
        """
        try:
            self.cursor.execute(sql)
            self.db.commit()
            mylog.info("Execute sql:{}" .format(sql))
            return self.cursor
        except Exception:
            self.db.rollback()
            mylog.error("Execute sql faild：{}" .format(sql))

    def fetchall(self, sql):
        """
        查询所有结果
        :param sql: 需要查询的sql
        :return: 所有查询结果
        """
        try:
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            mylog.info("Execute sql:{}".format(sql))
            return rows
        except Exception:
            mylog.error("Execute sql faild：{}".format(sql))

    # 查询一条结果
    def fetchone(self, sql):
        """
        查询一条结果
        :param sql: 需要查询的sql
        :return: 一条查询结果
        """
        try:
            self.cursor.execute(sql)
            row = self.cursor.fetchone()
            mylog.info("Execute sql:{}".format(sql))
            return row
        except Exception:
            mylog.error("Execute sql faild：{}".format(sql))

    # 关闭数据库
    def close(self):
        """
        关闭数据库连接
        """
        self.cursor.close()
        self.db.close()
        mylog.info("Disconnect database:{}".format(self.database))


if __name__ == '__main__':
    mysql = MySql()
    mysql.connect()
    insert_sql = '''INSERT INTO new_qiyi_user_vip_copy(user_id,deadline) VALUES('4005235','4299329932')'''
    mysql.execute(insert_sql)
    print(mysql.fetchone('SELECT * FROM new_qiyi_user_vip_copy'))
    delete_sql = '''DELETE FROM new_qiyi_user_vip_copy'''
    mysql.execute(delete_sql)
    print(mysql.fetchall('SELECT * FROM new_qiyi_user_vip_copy'))
    mysql.close()


