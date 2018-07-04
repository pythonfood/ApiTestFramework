#!/usr/bin/env python3
# coding:utf-8

from TestData import testdata
from TestSuite.testsuite import TestSuite
from Common.myemail import MyEmail
from Common.mylog import MyLog

mylog = MyLog().mylog()


def main():
    mylog.info('***************INIT DATABASE***************')
    testdata.clear_data()
    testdata.generate_data()

    mylog.info('***************TEST START***************')
    testsuite = TestSuite()
    report = testsuite.run()

    mylog.info('***************SEND REPORT***************')
    myemail = MyEmail()
    myemail.send(report)


if __name__ == '__main__':
    main()
