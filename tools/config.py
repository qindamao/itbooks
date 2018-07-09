#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#各类url
DOUBAN_SEARCH_URL = 'https://book.douban.com/subject_search?search_text={searchkey}&cat=1001'
DOUBAN_DETAIL_URL = 'https://book.douban.com/subject/{subjectcode}/'
BAIDU_URL = 'https://www.baidu.com/s'
#图书资源分类-关键字
'''
KAIFAYUYAN:开发语言类及平台
'''
# CLASSIFICATION = {
#     'KAIFAYUYAN':['Actionscript','C语言','C#','C++','java','JaveEE','Javascript','Perl','PHP','Python','VB',
#                   '.NET','Erlang','Ruby','HTML5','iOS','Android','汇编语言',' 嵌入式'],
#     'CAOZUOXITONG':['Linux',' MacOS','Solaris','Ubuntu','Unix','Windows Server','CentOS'],
#     'SHUJUKU':['数据库','Access','DB2','MongoDB','MySQL',' Oracle','Redis','SQLite','SQLServer','Sybase','SQL'],
#     'DASHUJU':['大数据','spark',' Hadoop','Hbase','Hive','Netty'],
#     'YUNJISUAN':['云计算','kubernetes','mesos','Docker','微服务','Openstack'],
#     'ANQUANJISHU':['网络攻防','网络安全','系统安全','信息安全'],
#     'KECHENG':['计算机原理','计算机导论','数据结构','软件工程','计算机网络','编译原理','密码学'],
#     'RENGONGZHINENG':['人工智能','机器学习','深度学习','搜索引擎','计算广告','VR'],
#     'QUKUAILIAN':['比特币','区块链','Dapp','BlueMix'],
#     'WANGLUOJISHU':['网络基础','网络监控',' 网络设备',' 系统集成','综合布线'],
#     'YOUXIKAIFA':['游戏开发','cocos2D','Unity3D','DirectX','WebGL']
# }
CLASSIFICATION = {
    'KAIFAYUYAN':['C语言','C#','C++','java','JaveEE','Javascript','Perl','PHP','Python','VB',
                  '.NET','Erlang','Ruby','HTML5','iOS','Android','汇编语言',' 嵌入式'],
    'CAOZUOXITONG':['Linux',' MacOS','Solaris','Ubuntu','Unix','Windows Server','CentOS'],
    'SHUJUKU':['数据库','Access','DB2','MongoDB','MySQL',' Oracle','Redis','SQLite','SQLServer','Sybase','SQL'],
    'DASHUJU':['大数据','spark',' Hadoop','Hbase','Hive','Netty'],
    'YUNJISUAN':['云计算','kubernetes','mesos','Docker','微服务','Openstack'],
    'ANQUANJISHU':['网络攻防','网络安全','系统安全','信息安全'],
    'KECHENG':['计算机原理','计算机导论','数据结构','软件工程','计算机网络','编译原理','密码学'],
    'RENGONGZHINENG':['人工智能','机器学习','深度学习','搜索引擎','计算广告','VR'],
    'QUKUAILIAN':['比特币','区块链','Dapp','BlueMix'],
    'WANGLUOJISHU':['网络基础','网络监控',' 网络设备',' 系统集成','综合布线'],
    'YOUXIKAIFA':['游戏开发','cocos2D','Unity3D','DirectX','WebGL']
}
#数据库配置
dbconfig = {
  'user': 'qindamao',
  'password': 'qin_XIA_2018',
  'host': '193.112.12.252',
  'database': 'vxzy',
  'raise_on_warnings': True,
}
#日志路径
LOG_PATH = 'D:\\log\\itbooks\\'