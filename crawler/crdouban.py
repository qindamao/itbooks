#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common import exceptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
from multiprocessing import Queue
from datetime import  datetime
import time
import re
import sys
import logging
import threading
sys.path.append('.')
sys.path.append('../tools')
import tools.headertool
import tools.config
from dbs.dbdouban import dbdouban

#logger = logging.getLogger('crdouban')
class crdouban:
    def __init__(self,q,searchkey = ''):
        self.__searchkey = searchkey
        self.__getstartpage()
        self.__q = q
    def __getstartpage(self):
        '''
        构造分类爬虫起始页路径
        '''
        self.__starturl = tools.config.DOUBAN_SEARCH_URL.format(searchkey = self.__searchkey)
    def startcrawl(self):
        self.__driver = webdriver.Chrome('chromedriver.exe')
        #self.__driver.get(self.__starturl)
        self.__driver.get('https://book.douban.com/subject_search?search_text=C%E8%AF%AD%E8%A8%80&cat=1001')
        self.__crawlpage()
    def __crawlpage(self):
        '''
        递归爬取每个查询列表的所有页
        '''
        try:
            #logging.info(logging.info('正在爬取的列表页地址{0}'.format(self.__driver.current_url)))
            print('正在爬取的列表页地址{0}'.format(self.__driver.current_url))
            csspager = WebDriverWait(self.__driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.paginator'))
                )
            if csspager:
                #处理当前页的数据
                self.__processdata()
                try:
                    WebDriverWait(self.__driver, 1).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, '.next.activate'))
                        )
                    #最后一页
                    self.__driver.quit()
                except exceptions.TimeoutException:
                    #说明还不是最后一页,休息一秒点击下一页继续爬
                    time.sleep(1)
                    self.__driver.find_element(By.CLASS_NAME,'next').click()
                    self.__crawlpage()
        except exceptions.TimeoutException:
            #如果当前页面因为超时没有加载出来，重新运行当前页面
            self.__crawlpage()

    def __processdata(self):
        '''
        查询列表页数据处理
        '''
        itemroots = self.__driver.find_elements(By.CLASS_NAME,'item-root')
        for item in itemroots:
            try:
                link = item.find_element(By.CLASS_NAME,'cover-link')
            except exceptions.NoSuchElementException as err:
                # 如果没有cover-link属性，说明不是书籍
                continue
            #如果是专栏，就与此不匹配
            if not re.match(r'https://book.douban.com/subject/(\d+)/',link.get_attribute('href')):
                continue
            subjectcode = re.match(r'https://book.douban.com/subject/(\d+)/',link.get_attribute('href')).groups()[0]
            covera = item.find_element(By.CLASS_NAME,'cover')
            coverurl = ''
            if covera:
                coverurl = item.find_element(By.CLASS_NAME,'cover').get_attribute('src')
            bookname = item.find_element(By.CLASS_NAME,'title-text').text
            pl = item.find_element(By.CLASS_NAME,'pl').text
            score = ''
            level = 1
            if pl == '(评价人数不足)':
                level = 2
            elif pl == '(目前无人评价)':
                level = 3
            if level == 1:
                score = item.find_element(By.CLASS_NAME,'rating_nums').text
            self.__q.put(subjectcode)
            db = dbdouban()
            t1 = threading.Thread(target=db.create_book, args=(bookname,subjectcode,level,self.__searchkey,score,coverurl))
            t1.start()
            t1.join()
            #db.create_book(bookname,subjectcode,level,self.__searchkey,coverurl)
    def crawldetail(self,subcode):
        durl = tools.config.DOUBAN_DETAIL_URL.format(subjectcode=subcode)
        #logging.info(logging.info('正在爬取的详情页地址{0}'.format(durl)))
        print('正在爬取的详情页地址{0}'.format(durl))
        headers = tools.headertool.randHeader()
        headers['Host'] = 'book.douban.com'
        r = requests.get(url= durl,headers=headers)
        soup = BeautifulSoup(r.text,'lxml')
        title = soup.find('h1').get_text()
        node = soup.find('span', class_='pl',text = re.compile('\w*作者'))
        author = ''
        if node:
            author = node.next_sibling.next_sibling.get_text().strip().replace('\n','')
        pages = ''
        node = soup.find('span', class_='pl',text = re.compile('页数:'))
        if node:
            pages = node.next_sibling.strip()
        ISBN = ''
        node = soup.find('span', class_='pl',text = re.compile('ISBN:'))
        if node:
            ISBN = node.next_sibling.strip()
        price = ''
        node = soup.find('span', class_='pl',text = re.compile('定价:'))
        if node:
            price = node.next_sibling.strip()
        nodes = soup.find_all('div',class_='intro')
        intro = ''
        if nodes:
            for node in nodes:
                intro = intro + node.get_text()
            if len(intro) > 5000:
                intro = intro[:4990] + '...'
        catalog = ''
        node = soup.find('div',class_='indent',id=re.compile(r'dir_\d+_full'))
        if node:
            catalog = re.match('<div class="indent" id="dir_\d+_full" style="display:none">(.*?)</div>',str(node).replace('\n','')).group(1)
            if len(catalog) > 5000:
                catalog = catalog[:4990] + '...'
        node = soup.find('span', class_='pl',text = re.compile('出版年:'))
        publishyear = ''
        if node:
            publishyear = node.next_sibling.strip()
        tags = ''
        nodes = soup.find_all('a',class_='tag')
        if nodes:
            tags = ','.join([node.get_text().strip() for node in nodes])
        db = dbdouban()
        t1 = threading.Thread(target=db.update_douban_detail, args=(subcode,author,pages,ISBN,price,intro,catalog,publishyear,tags,datetime.now().strftime('%Y-%m-%d')))
        t1.start()
        t1.join()
        #db.update_douban_detail(subcode,author,pages,ISBN,price,intro,catalog,publishyear,tags,datetime.now().strftime('%Y-%m-%d'))
        #print('title:%s,author:%s,pages:%s,ISBN:%s,price:%s,publishyear:%s,tags:%s'%(title,author,pages,ISBN,price,publishyear,tags))

if __name__ == '__main__':
    q = Queue()
    douban = crdouban(q)
    douban.startcrawl()
    #douban.crawldetail('https://book.douban.com/subject/24534868/')

    