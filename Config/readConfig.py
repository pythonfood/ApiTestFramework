#!/usr/bin/env python3
# coding:utf-8

import os
import configparser
from Common.mylog import MyLog

mylog = MyLog().mylog()

# 注意：这里不要使用os.getcwd()，模块被引用后，获取的是外层调用的脚本路径
current_path = os.path.dirname(os.path.realpath(__file__))  # 脚本所在当前路径
config_path = os.path.join(current_path, 'config.ini')  # 配置文件路径


class ReadConfig:
    """读取和写入配置文件"""

    def __init__(self):
        """
        初始化读取配置文件内容
        """
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

    def mysql(self, name):
        """
        读取mysql配置文件内容
        :param name: 名称
        :return: 返回值
        """
        value = self.config.get('MYSQL', name)
        return value

    def http(self, name):
        """
        读取http配置文件内容
        :param name: 名称
        :return: 返回值
        """
        value = self.config.get('HTTP', name)
        return value

    def headers(self):
        """
        读取header配置文件内容
        :return: items全部内容
        """
        items = self.config.items('HEADERS')
        return items

    def email(self, name):
        """
        读取email配置文件内容
        :param name: 名称
        :return: 返回值
        """
        value = self.config.get('EMAIL', name)
        return value

    def write_config(self, section, name, value):
        """
        写入配置文件
        :param section: 选项
        :param name: 名称
        :param value: 返回值
        :return:
        """
        self.config.set(section, name, value)
        try:
            with open(config_path, 'w+') as fw:
                self.config.write(fw)
            mylog.info('Set config.ini [{section}]:{name}={value}'.format(section=section, name=name, value=value))
        except Exception:
            mylog.error('Set config.ini [{section}]:{name}={value} faild !'.format(section=section, name=name, value=value))


if __name__ == '__main__':
    readconfig = ReadConfig()
    print(readconfig.mysql('host'))
    print(readconfig.http('host'))
    print(readconfig.email('subject'))
    readconfig.write_config('HEADERS', 'token', 'hk43h5j3j2k3k2')
    print(dict(readconfig.headers()))


