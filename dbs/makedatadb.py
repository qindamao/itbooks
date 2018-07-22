#! /usr/bin/env.python
# -*-coding: utf-8 -*-
# __author__ = "qindamao"
# Date: 2018/7/13

import mysql.connector
from dbs import dbbase

class makedatadb:
    def __init__(self):
        pass
    def get_all_tags(self):
        db = dbbase()
        sql = 'select tags from itbooks_star where isdelete = 0'
        try:
            db.openconnection()
            cursor = db.opencursor()[0]
            cursor.execute(sql)
            items = cursor.fetchall()
            if len(items) > 0:
                return  [item[0] for item in items]
            return None
        except mysql.connector.Error as err:
            #logger.exception('update_douban_detail:{0}'.format(err))
            print('get_no_details:{0}'.format(err))
        finally:
            db.close()

    def get_all_booknames(self):
        db = dbbase()
        sql = 'select subjectcode,bookname from itbooks_star where isdelete = 0'
        try:
            db.openconnection()
            cursor = db.opencursor()[0]
            cursor.execute(sql)
            items = cursor.fetchall()
            if len(items) > 0:
                return  [item[0] + ',' + item[1] for item in items]
            return None
        except mysql.connector.Error as err:
            #logger.exception('update_douban_detail:{0}'.format(err))
            print('get_all_booknames:{0}'.format(err))
        finally:
            db.close()
    def delete_the_dirty(self,dirtydata):
        db = dbbase()
        sql = 'update itbooks_star set isdelete = 1 where subjectcode =%s'
        try:
            db.openconnection()
            cursor = db.opencursor()[0]
            cursor.execute(sql,(dirtydata,))
            db.cnx.commit()
        except mysql.connector.Error as err:
            #logger.exception('update_douban_detail:{0}'.format(err))
            print('delete_the_dirty:{0}'.format(err))
        finally:
            db.close()

