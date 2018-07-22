#! /usr/bin/env.python
# -*-coding: utf-8 -*-
# __author__ = "qindamao"
# Date: 2018/7/14

import mysql.connector
from dbs import dbbase

class dbbaidu:
    def __init__(self):
        pass
    def get_nocsdn_bookname(self):
        '''
        查询还没有爬过baidu csdn的书名
        :return:list (bookname，subjectcode)
        '''
        db = dbbase()
        sql = 'select bookname,subjectcode from itbooks_star where isdelete = 0 and csdnsearhced = 0'
        try:
            db.openconnection()
            cursor = db.opencursor()[0]
            cursor.execute(sql)
            items = cursor.fetchall()
            return items
        except mysql.connector.Error as err:
            #logger.exception('update_douban_detail:{0}'.format(err))
            print('get_nocsdn_bookname:{0}'.format(err))
        finally:
            db.close()
    def update_csdn_info(self,csdnurl,csdnscore,subcode):
        '''
        更新爬到的csdn连接和资源评分
        :param csdnurl:
        :param csdnscoure:
        :param subcode:
        :return:
        '''
        db = dbbase()
        sql = 'update itbooks_star set csdnscore = %s , csdnurl =%s , csdnsearhced = 1 where subjectcode =%s '
        try:
            db.openconnection()
            cursor = db.opencursor()[0]
            cursor.execute(sql,(csdnscore,csdnurl,subcode))
            db.cnx.commit()
        except mysql.connector.Error as err:
            #logger.exception('update_douban_detail:{0}'.format(err))
            print('update_csdn_info:{0}'.format(err))
        finally:
            db.close()

