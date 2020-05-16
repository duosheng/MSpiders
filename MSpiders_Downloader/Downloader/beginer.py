# encoding=utf-8
# ---------------------------------------
#   语言：Python2.7
#   日期：2017-07-10
#   作者：九茶<bone_ace@163.com>
#   功能：
# ---------------------------------------


import sys
import time
import logging
from imp import reload

import gevent
from gevent import monkey

from MSpiders_Downloader.Downloader.logs.log_init import logger
from MSpiders_Downloader.Downloader.utils.DingDingRobot import sendMsg
from MSpiders_Downloader.Downloader.crawlers.CrawlerFactory import CrawlerFactory
from MSpiders_Downloader.Downloader.dns_cache.dns_cache import _setDNSCache
from MSpiders_Downloader import settings
from multiprocessing import Process, sharedctypes

from common.queues.Queue_Factory import QueueFactory

reload(sys)
# monkey.patch_all()
crawlerFactory = CrawlerFactory()
queueFactory = QueueFactory()
queue_seed = queueFactory.create(dbType=settings.Queue_seed_type, host=settings.Queue_seed_host, port=settings.Queue_seed_port, password=settings.Queue_seed_password)
queue_html = queueFactory.create(dbType=settings.Queue_html_type, host=settings.Queue_html_host, port=settings.Queue_html_port, password=settings.Queue_seed_password)


def pipeline_item(items, seed_packed):
    size_characters = 0
    for item in items:
        try:
            if len(item) == 0 or item['html'] is None:  # 这是一条异常
                seed_packed['failureCount'] = seed_packed['failureCount'] + 1 if 'failureCount' in seed_packed.keys() else 1
                queue_seed.put(seed_packed, keyName='Failure:%s' % seed_packed['spider'].split('.')[0].replace('Spider_', ''))
                errorCount = queue_seed.incr(1, keyName='ErrorCount:Downloader:%s' % seed_packed['spider'].split('.')[0].replace('Spider_', ''))
                if errorCount >= settings.ERRORMAX:
                    sendMsg('Downloader - %s error num up to %s' % (seed_packed['spider'], errorCount))
                logger.error('Seed-Failed: %s - %s' % (seed_packed['spider'], seed_packed['url']))
                break
            if len(item['html']) > 0:
                queue_seed.setZero(keyName='ErrorCount:Downloader:%s' % seed_packed['spider'].split('.')[0].replace('Spider_', ''))
                queue_seed.incr(1, keyName='Sum:Downloader:%s' % seed_packed['spider'].split('.')[0].replace('Spider_', ''))
                size_characters += len(item['html'])
                if 'parser' not in item.keys():
                    item['parser'] = seed_packed['spider'].split('.')[0].replace('Spider', 'Parser')
                item['url'] = seed_packed['url']
                item['time_crawl'] = int(time.time())
                queue_html.put(item, keyName=settings.Queue_html_keyName)
        except Exception as e:
            logger.error(e)
    return size_characters


def run(pages):
    """ 每执行一次run()，处理一条Seed """
    logger = logging.getLogger('root')
    try:
        txt = queue_seed.get(keyName=settings.Queue_seed_keyName)
        seed_packed = eval(txt[1] if isinstance(txt, tuple) else txt)
    except Exception as e:
        logger.error('Get seed from redis error - %s' % str(e))
        return
    if seed_packed:
        _setDNSCache()  # DNS解析缓存
        if '.' in seed_packed['spider']:
            spider_name, method_name = seed_packed['spider'].split('.')
        else:
            spider_name = seed_packed['spider']
            method_name = 'crawl0'
        spider = crawlerFactory.createObject(objectName=spider_name)
        method = crawlerFactory.createMethod(object=spider, methodName=method_name)
        if method is None:
            # 使用通用下载器
            logger.warning('With no method: %s' % str(seed_packed))
        else:
            try:
                items = method(seed_packed)
            except Exception as e:
                logger.error('your spider error - %s' % str(e))
                items = [{'html': None}]
            try:
                pages.value += len(items)
                size_characters = pipeline_item(items, seed_packed)
                debug_msg = ('Crawled URL:%(url)s\nSpider_name:%(spider)s\nNum_html:%(num_html)s\nSize_characters:%(size)s\n')
                debug_args = {'url': seed_packed['url'], 'spider': spider_name, 'num_html': len(items), 'size': size_characters}
                logger.debug(debug_msg, debug_args)
            except Exception as e:
                logger.error('deal spider result error - %s' % str(e))


def keep_log(pages):
    """ 功能：INFO级别的日志监控，显示每分钟的抓取量 """
    logger = logging.getLogger('root')
    pagesprev = 0
    logger.warning('Now,Start:')
    while True:
        speed_page = pages.value - pagesprev
        pagesprev = pages.value
        msg = ('Crawled: %(num_page)s pages( %(speed_page)s pages/min)')
        log_args = {'num_page': pagesprev, 'speed_page': speed_page}
        logger.warning(msg, log_args)
        time.sleep(60)


def pre_run(pages):
    """ 在每个进程里面再启动多协程 """
    logger = logging.getLogger('root')
    try:
        while True:  # 在此处循环而不在run里加循环的原因是：可以设置协程超时时间，回收死掉的协程
            threads = [gevent.spawn(run, pages) for _ in range(settings.Num_gevent)]
            gevent.joinall(threads, timeout=settings.Timeout_gevent)
    except Exception as e:
        logger.error('One thread has downed!Reason:' + str(e))


def begin():
    """ 启动多进程 """
    plist = []
    pages = sharedctypes.Value('l', 0, lock=False)
    p = Process(target=keep_log, args=(pages,))
    p.start()
    plist.append(p)
    for i in range(settings.Num_process):
        p = Process(target=pre_run, args=(pages,))
        p.start()
        plist.append(p)
    for p in plist:
        p.join()

