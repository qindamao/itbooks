#! /usr/bin/env.python
# -*-coding: utf-8 -*-
# __author__ = "qindamao"
# Date: 2018/7/7
import mysql.connector
import logging
from dbs import dbbase

#logger = logging.getLogger('csdndb')
class dbdouban:
    def __init__(self):
        pass
    def create_book(self,bookname,subjectcode,level,searchkey,doubanscore,cover):
        '''
        从豆瓣列表爬取得内容创建一本书
        :param bookname:
        :param subjectcode:
        :param level:
        :param searchkey:
        :return:
        '''
        db = dbbase()
        sql1 = 'select count(*) from itbooks where subjectcode = %s'
        sql2 = 'insert into itbooks(bookname,subjectcode,level,searchkey,doubanscore,cover) values(%s,%s,%s,%s,%s,%s)'
        try:
            db.openconnection()
            cursor1 = db.opencursor()[0]
            cursor1.execute(sql1,(subjectcode,))
            res = cursor1.fetchone()
            if res[0] == 0:
                cursor2 = db.opencursor()[1]
                cursor2.execute(sql2, (bookname, subjectcode,level,searchkey,doubanscore,cover))
                db.cnx.commit()
        except mysql.connector.Error as err:
            #logger.exception('create_book:{0}'.format(err))
            print('create_book:{0}'.format(err))
        finally:
            db.close()

    def update_douban_detail(self,subjectcode,author,pages,ISBN,price,introduction,catalog,publishyear,tags,lastupdate):
        db = dbbase()
        sql = '''update itbooks 
                set author=%s,pages=%s,ISBN=%s,price=%s,
                introduction=%s,catalog=%s,publishyear=%s,tags=%s
                ,lastupdate =%s where subjectcode = %s'''
        try:
            db.openconnection()
            cursor = db.opencursor()[0]
            cursor.execute(sql,(author,pages,ISBN,price,introduction,catalog,publishyear,
                                tags,lastupdate,subjectcode))
            db.cnx.commit()
        except mysql.connector.Error as err:
            #logger.exception('update_douban_detail:{0}'.format(err))
            print('update_douban_detail:{0}'.format(err))
        finally:
            db.close()
if __name__ == '__main__':
    dbdb = dbdouban()
    #dbdb.create_book('流畅的python','8857833',1,'python','9.0')
    dbdb.update_douban_detail('8857833','xiaqin','200','7485949349','45.00元',
                              '介绍介绍','目录目录','2016-3-3','9.0','python,编程,计算机','2017-07-08')

