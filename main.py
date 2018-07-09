from multiprocessing import Process, Queue
import os, time, random
import logging
import logging.config
import cloghandler
from logging.handlers import TimedRotatingFileHandler
from functools import reduce
from crawler.crdouban import crdouban
from tools.config import LOG_PATH,CLASSIFICATION
# 写数据进程执行的代码:

# Create the filter.


# logging.config.dictConfig({
#     'version': 1,
#     'disable_existing_loggers': True,
#     'formatters': {
#         'verbose': {
#             'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
#             'datefmt': "%Y-%m-%d %H:%M:%S"
#         },
#         'simple': {
#             'format': '%(levelname)s %(message)s'
#         },
#     },
#     'handlers': {
#         'null': {
#             'level': 'DEBUG',
#             'class': 'logging.NullHandler',
#         },
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#             'formatter': 'verbose'
#         },
#         'file': {
#             'level': 'DEBUG',
#             'class': 'cloghandler.ConcurrentRotatingFileHandler',
#             # 当达到10MB时分割日志
#             'maxBytes': 1024 * 1024 * 10,
#             # 最多保留50份文件
#             'backupCount': 50,
#             # If delay is true,
#             # then file opening is deferred until the first call to emit().
#             'delay': True,
#             'filename': LOG_PATH + 'mylog.log',
#             'formatter': 'verbose'
#         }
#     },
#     'loggers': {
#         '': {
#             'handlers': ['file'],
#             'level': 'INFO',
#         },
#     }
# })

def should_log(record):  
    """Return whether a logging.LogRecord should be logged."""  
    # FIXME: Enable the logging of autoinstall messages once  
    #        autoinstall is adjusted.  Currently, autoinstall logs  
    #        INFO messages when importing already-downloaded packages,  
    #        which is too verbose.  
    if record.name.startswith("schedule"):  
        return False  
    return True


def init():
    if not os.path.exists(LOG_PATH):
        os.makedirs(LOG_PATH)

    # fileTimeHandler = TimedRotatingFileHandler(LOG_PATH + 'mylog', 'midnight', 1, 10)
    # fileTimeHandler.suffix = "%Y%m%d%H%M%S.log"
    # fileTimeHandler.addFilter(should_log)
    # logging.basicConfig(level=logging.INFO,
    #                     format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    #                     datefmt='%Y-%m-%d %H:%M:%S',
    #                     handlers=[fileTimeHandler])

def scawllistpage(q,searchkeys):
    #logging.info('scawllistpage启动，进程号:%s'%os.getpid())
    print('scawllistpage启动，进程号:%s'%os.getpid())
    for searchkey in searchkeys:
        #logging.info('正在爬取关键字：%s' % searchkey)
        print('正在爬取关键字：%s' % searchkey)
        douban = crdouban(q,searchkey)
        douban.startcrawl()
    q.put('END')
def scawldetailpage(q):
    print('scawldetailpage启动，进程号:%s'%os.getpid())
    while True:
        subcode = q.get(True)
        print(subcode)
        if subcode == 'END':
            break
        douban = crdouban(q)
        douban.crawldetail(subcode)

def getkeylist(x,y):
    return x + y
if __name__=='__main__':
    searchkeys = reduce(getkeylist,[x for x in CLASSIFICATION.values()])
    init()
    q = Queue()
    #logging.info('主进程启动...')
    print('主进程启动...')
    lp = Process(target=scawllistpage,args=(q,searchkeys))
    dp = Process(target=scawldetailpage,args=(q,))
    lp.start()
    dp.start()
    lp.join()
    dp.join()
    #logging.info('主进程停止...')
    print('主进程停止...')
