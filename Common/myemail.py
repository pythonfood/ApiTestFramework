#!/usr/bin/env python3
# coding:utf-8

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from Common.mylog import MyLog
from Config.readConfig import ReadConfig

mylog = MyLog().mylog()

readconfig = ReadConfig()  # 声明读取配置文件对象


class MyEmail:
    """设置邮件头、设置邮件内容、添加邮件附件、发送邮件"""

    def __init__(self):
        """
        email相关初始化
        """
        self.host = readconfig.email('host')
        self.port = readconfig.email('port')
        self.user = readconfig.email('user')
        self.password = readconfig.email('password')
        self.sender = readconfig.email('sender')
        self.subject = readconfig.email('subject')
        self.contents = readconfig.email('content')
        # 获取收件人列表
        self.receiver = readconfig.email('receiver')
        self.receivers = []
        for recv in str(self.receiver).split(';'):
            self.receivers.append(recv)
        # 定义邮件实例
        self.msg = MIMEMultipart('related')

    def header(self):
        """
        设置邮件头
        :return:
        """
        self.msg['from'] = self.sender
        self.msg['subject'] = self.subject
        self.msg['to'] = ';'.join(self.receivers)  # 添加收件人列表

    def content(self):
        """
        设置邮件内容
        :return:
        """
        content_plain = MIMEText(self.contents, 'plain', 'utf-8')
        self.msg.attach(content_plain)

    def file(self, report):
        """
        添加邮件附件
        :param report: 测试报告文件
        :return:
        """
        with open(report, 'rb') as f:
            report_file = MIMEText(f.read(), 'base64', 'utf-8')
            report_file["Content-Type"] = "application/octet-stream"
            report_file["Content-Disposition"] = 'attachment; filename="{}"'.format(os.path.basename(report))
            self.msg.attach(report_file)

    def send(self, report):
        """
        发送邮件
        :param report: 测试报告文件
        :return:
        """
        self.header()
        self.content()
        self.file(report)
        try:
            smtp = smtplib.SMTP()
            smtp.connect(self.host, self.port)
            smtp.login(self.user, self.password)
            smtp.sendmail(self.sender, self.receivers, self.msg.as_string())
            smtp.quit()
            mylog.info('Send test report email:{}'.format(os.path.basename(report)))
        except Exception:
            mylog.error('Send test report email:{} faild !'.format(os.path.basename(report)))


if __name__ == '__main__':
    myemail = MyEmail()
    myemail.send(r'D:\PycharmProjects\TestFramework\Report\TestResult .html')



