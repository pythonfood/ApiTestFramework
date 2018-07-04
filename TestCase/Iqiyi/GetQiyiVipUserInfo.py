# !/usr/bin/env python3
# coding:utf-8

import unittest
import requests
from parameterized import parameterized
from TestData import testdata
from Common.mylog import MyLog
from Common.myhttp import MyHttp

mylog = MyLog().mylog()
test_data = testdata.read_data('getQiyiVipUserInfo.xlsx', '获取爱奇艺会员到期时间接口')[1:]  # 测试数据，去除首行字段行


def testcase_name(testcase_func, param_num, param):
    """
    设置测试用例名称，便于在测试报告中展示
    注：修改了parameterized的源代码，测试用例名称中可以用中文

    :param testcase_func: 测试方法名称
    :param param_num: 参数序号
    :param param: 传入参数
    :return: 格式化后的用例名称
    """
    return "%s_%s" % (
        testcase_func.__name__,
        parameterized.to_safe_name(str(param_num) + '_' + str(param.args[0])),
    )


class TestCase(unittest.TestCase):
    def setUp(self):
        self.myhttp = MyHttp()
        self.myhttp.write_token()  # 获得最新token写入配置文件

    def tearDown(self):
        pass

    @parameterized.expand(test_data, testcase_func_name=testcase_name)  # 调用数据的传参必须和数据一一对应
    def test(self, case_name, url_supplement, method, generate_data, token, userId, version, status_code, code, success, message, result, deadline):
        mylog.info('Run test case:{}'.format(case_name))
        print('\n【Request】')

        self.data = '/' + str(userId) + '-' + str(version) + '.json'  # 拼接参数
        print('* params:', self.data)
        self.url = self.myhttp.url(url_supplement=url_supplement) + self.data  # url由path路径和参数共同组成
        print('* url:', self.url)
        mylog.info('url:{}'.format(self.url))

        self.headers = self.myhttp.headers
        print('* headeres:', self.headers)
        mylog.info('headeres:{}'.format(self.headers))

        response = requests.get(url=self.url, headers=self.headers)
        print('【response】')

        self.assertEqual(status_code, response.status_code)  # 断言状态码
        mylog.info('status_code:{}'.format(status_code))
        if status_code == 200:
            res = response.json()  # 状态码200的才解析成json()格式
            print(res)
            mylog.info('response:{}'.format(res))

            print('【Expect】')
            print('* status_code:', status_code)
            self.assertEqual(code, res['data']['code'])
            print('* code:', code)
            self.assertEqual(bool(success), res['data']['success'])
            print('* success:', bool(success))
            self.assertEqual(message, res['data']['message'])
            print('* message:', message)
            if result == 'null':
                self.assertEqual(None, res['data']['result'])  # 如果预期result为null,则断言result是否为None
                print('* result:', None)
            else:
                self.assertEqual(str(deadline), res['data']['result']['deadline'])  # result不为空，则断言具体字段
                print('* deadline:', deadline)
        else:
            print('【Expect】')
            print('* status_code:', status_code)
            res = response.text  # 状态码不是200的，不需要json验证了
            print(res)
            mylog.info('response:{}'.format(res))


if __name__ == '__main__':
    unittest.main(verbosity=2)  # Pycharm执行时注意：鼠标需要放在unittest.main(verbosity=2)代码块的位置，否则会报错
