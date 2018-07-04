#!/usr/bin/env python3
# coding:utf-8

import requests
from Common.mylog import MyLog
from Config.readConfig import ReadConfig

mylog = MyLog().mylog()

readconfig = ReadConfig()


class MyHttp:
    """http请求相关url、headers、timeout、获取最新token"""

    def __init__(self):
        """
        http请求相关初始化
        """
        self.scheme = readconfig.http('scheme')
        self.host = readconfig.http('host')
        self.port = readconfig.http('port')
        self.full_url = None
        self.timeout = readconfig.http('timeout')
        self.headers = dict(readconfig.headers())

    def url(self, url_supplement=''):
        """
        拼接完整url
        :param url_supplement: url补充部分
        :return: 完整url
        """
        self.full_url = self.scheme + '://' + self.host + ':' + self.port + url_supplement
        return self.full_url

    def write_token(self, login_url='/login', username='admin', password='123456'):
        """
        获取最新token，并写入配置文件
        :param login_url: 登录url
        :param username: 用户名
        :param password: 密码
        :return:
        """
        login_url = self.url(login_url)
        headers = self.headers
        data = {
            'username': username,
            'password': password
        }
        response = requests.post(url=login_url, json=data, headers=headers)
        if response.status_code == 200:
            try:
                token = response.json()['data']['token']
                mylog.info('Get new token:{}'.format(token))
                readconfig.write_config('HEADERS', 'token', token)
                self.headers = dict(readconfig.headers())  # 修改config.ini文件后重新获取下headers
            except Exception:
                mylog.error('Get new token faild !')
        else:
            mylog.error('Get new token faild !')


if __name__ == '__main__':
    myhttp = MyHttp()
    url = myhttp.url('/src/img.png')
    print(url)
    print(myhttp.headers)
    print(myhttp.timeout)
    myhttp.write_token()
    print(myhttp.headers)
