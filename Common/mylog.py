#!/usr/bin/env python3
# coding:utf-8

import os
import time
import logging
import threading

current_path = os.path.dirname(os.path.realpath(__file__))  # 脚本所在当前路径
log_path = os.path.join(os.path.dirname(current_path), 'Log')  # 日志保存路径
# 如果日志路径不存在，则自动创建
if not os.path.exists(log_path):
    os.mkdir(log_path)


class Log:
    def __init__(self):
        """
        日志相关初始化
        """
        # 日志文件名称格式化
        self.logname = os.path.join(log_path, '{}.log'.format(time.strftime('%Y%m%d_%H%M%S')))
        # 定义logger实例
        self.logger = logging.getLogger()
        # 定义打印信息级别
        self.logger.setLevel(logging.INFO)
        # 定义日志格式化
        self.formatter = logging.Formatter('%(asctime)s- %(filename)s(%(lineno)d)- %(levelname)s- %(message)s')
        # 定义FileHandler，用于写到本地
        self.file_handler = logging.FileHandler(self.logname, 'a', encoding='utf-8')
        # 设置FileHandler日志格式化
        self.file_handler.setFormatter(self.formatter)
        # logger添加FileHandler
        self.logger.addHandler(self.file_handler)


class MyLog:
    """单独启用线程写入日志信息"""

    log = None
    mutex = threading.Lock()  # 互斥锁

    @staticmethod
    def mylog():
        """
        利用互斥锁来保证共享数据操作的完整性
        :return: 日志logger
        """
        if MyLog.log is None:
            MyLog.mutex.acquire()  # 锁占用
            MyLog.log = Log()
            MyLog.mutex.release()  # 锁释放
        return MyLog.log.logger


if __name__ == '__main__':
    mylog = MyLog().mylog()
    mylog.debug('调试级别日志测试')
    mylog.info('信息级别日志测试')
    mylog.warning('警告级别日志测试')
    mylog.error('错误级别日志测试')