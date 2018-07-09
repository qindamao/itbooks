#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common import exceptions
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
import re
import sys
sys.path.append('.')
import tools.config
import tools.headertool

class crbaidu:
    def __init__(self):
        # chrome_options = Options()
        # chrome_options.add_argument('--headless')
        # self.__driver = webdriver.Chrome('chromedriver.exe',chrome_options = chrome_options)
        self.__driver = webdriver.Chrome('chromedriver.exe')
        self.__driver.get(tools.config.BAIDU_URL)
        self.__rawcookies = self.__driver.get_cookies()
        self.__make_cookies()
        self.__driver.quit()
    def baidusearch(self,searchkey = ''):
        '''
        输入关键字，启动百度搜索
        :param searchkey:查询条件
        :return:None
        '''
        headers = tools.headertool.randHeader()
        data = {'ie':'utf-8','wd':'site:(download.csdn.net) {searchkey}'.format(searchkey = searchkey)}
        headers['Referer'] = 'https://www.baidu.com/'
        headers['Host'] = 'www.baidu.com'
        #headers['Cookie'] = 'BAIDUID=7105699E9260EEF577A2AB53E7394107:FG=1; BIDUPSID=7105699E9260EEF577A2AB53E7394107; PSTM=1529326728; BD_UPN=1352; ispeed_lsm=2; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=1466_21116_26350_20929; H_PS_645EC=3fed92UBX626LbTqSTRs2JoGt7WouJFOA2DukM%2BTzJnoMzy%2F%2FtbTMmwUA34; BD_CK_SAM=1; PSINO=3; BDSVRTM=112; WWW_ST=1530878327242'
        r = requests.get('https://www.baidu.com/s',headers = headers,params = data,cookies = self.__cookies)
        return self.__processbaidudata(r.text)
    def __processbaidudata(self,rawtext):
        '''
        百度搜索后，数据处理
        :param rawtext:百度搜索返回的页面源码
        :return:返回通过百度找到的csdn评分最高的资源(csdn链接,csdn资源评分)
        '''
        headers = tools.headertool.randHeader()
        soup = BeautifulSoup(rawtext, 'lxml')
        items = soup.find_all('div',class_='result c-container ')
        bestresource = ('',0)
        for item in items[:5]:
            baiduurl = item.find('a')['href']
            csdnitem = self.__processcsdndata(baiduurl,headers)
            if csdnitem[1] > bestresource[1]:
                bestresource = csdnitem
                if bestresource[1] == 5:
                    return bestresource
        if bestresource[1] < 4:
            return None
    def __processcsdndata(self,baiduurl,headers):
        '''
        处理csdn中的数据
        :param baiduurl:百度搜索中的连接
        :param headers:http请求头
        :return:(csdn链接,csdn资源评分)
        '''
        r = requests.get(baiduurl, headers=headers)
        csdnurl = r.url
        soup = BeautifulSoup(r.text,'lxml')
        score = soup.find('span',text=re.compile(r'综合评分：')).parent.find('em').get_text()
        if re.match('\d+',score):
            score = int(score)
        return (csdnurl,score)
    def __make_cookies(self):
        new_ck={}  
        for ck in self.__rawcookies:
            new_ck[ck['name']] = ck['value']
        self.__cookies = new_ck
if __name__ == '__main__':
    baidu = crbaidu()
    best = baidu.baidusearch('Python编程：从入门到实践')
    print(best)
