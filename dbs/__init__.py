#! /usr/bin/env.python
# -*-coding: utf-8 -*-
# __author__ = "qindamao"
# Date: 2018/7/7

import mysql.connector
import  sys
sys.path.append('.')
from tools.config import dbconfig
class dbbase:
  def __init__(self):
    self.cursor = []
    self.cnx = None
  def openconnection(self):
    self.cnx = mysql.connector.connect(**dbconfig)
  def opencursor(self,buffered=False):
    if buffered:
        self.cursor.append(self.cnx.cursor(buffered = True))
    else:
        self.cursor.append(self.cnx.cursor())
    return self.cursor
  def close(self):
    for c in self.cursor:
      c.close()
      self.cursor = []
    self.cnx.close()