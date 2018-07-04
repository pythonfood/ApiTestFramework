# 接口自动化测试框架

第一个手搭python+unittest接口自动化测试框架，实现测试数据和测试脚本分离，很多地方存在不足，请多指教，后续持续优化。

## 准备工作

安装需要的软件包：`pip install -r requirements.txt`

## 运行脚本

进入项目目录，执行：`python run.py`

## 框架简介

### Common

通用操作：

* HTMLTestRunner.py 用于生成测试报告
* myemail.py 发送测试报告邮件，相关配置在config.ini里设置
* myexcel.py 读取测试数据excel表格
* myhttp.py 网络请求的相关操作，相关配置在config.ini里设置
* mylog.py 输出执行过程的日志
* mysql.py 数据库相关操作，，相关配置在config.ini里设置
* myxml.py 读取测试数据对应数据库的xml配置文件

### Config

配置文件：

* config.ini 所有静态配置文件
* readConfig.py 读取和写入配置文件

### Continuous

持续集成环境：暂未实现。目前在jekins配置触发条件，执行run.py脚本即可。

### Log

执行日志：存储所有测试日志，单独启用一个线程打印日志。

### Report

测试报告：存储所有测试报告。

### Statistics

统计中心：暂未实现。目的：统计结果、分析、对比、反馈。

### TestCase

测试用例：

* 每个文件夹对应不同功能模块的测试用例。
* caselist.txt 记录待执行测试用例列表，用#号屏蔽的用例代表本轮不执行。

### TestData

测试数据：

* CaseData 存储所有测试数据excel表格。
* CaseDatabase 存储测试数据对应数据库的xml配置文件。
* testdata.py 读取测试数据、初始化数据库数据。

### TestSuit

测试组件：

* testsuite.py 根据caselist.txt装载测试用例，执行用例并生成测试报告。

### run.py

执行脚本：初始化数据库 ——> 执行测试用例 ——> 发送测试报告。
