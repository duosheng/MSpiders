# encoding=utf-8

import sys
import time
import json
from importlib import reload

import gevent
import logging
from MSpiders_Analyzer.Analyzer.utils.DingDingRobot import sendMsg
from MSpiders_Analyzer.Analyzer.parsers.ParserFactory import ParserFactory
from MSpiders_Analyzer.Analyzer.filter.filter import BloomFilter
from MSpiders_Analyzer import settings
from multiprocessing import Process, sharedctypes

# reload(sys)
# sys.setdefaultencoding('utf8')
# monkey.patch_all()
from common.queues.Queue_Factory import QueueFactory

DBS = {}
QUEUES = {'mongo': 'Queue_MongoDB', 'es': 'Queue_ElasticSearch', 'hbase': 'Queue_HBase', 'redis': 'Queue_Redis', 'ssdb': 'Queue_SSDB', 'mysql': 'Queue_MySQL', 'ffwb': 'Queue_FFWB'}
parserFactory = ParserFactory()
queueFactory = QueueFactory()
queue_seed = queueFactory.create(dbType=settings.Queue_seed_type, host=settings.Queue_seed_host, port=settings.Queue_seed_port, password=settings.Queue_seed_password)
queue_html = queueFactory.create(dbType=settings.Queue_html_type, host=settings.Queue_html_host, port=settings.Queue_html_port, password=settings.Queue_html_password)
FILTER = BloomFilter(host=settings.Filter_host, port=settings.Filter_port, db=settings.Filter_db, key=settings.Filter_keyName, password=settings.Filter_password)  # 基于Redis的BloomFilter去重对象



def pipeline_items(items, parser_name):
    """ 将解析出来的字段信息写入DB """
    logger = logging.getLogger('root')
    num_items = 0
    settings_temp = getattr(settings, parser_name)
    for item in items:
        if len(item.__dict__) == 0:  # 这是一条异常
            errorCount = queue_seed.incr(1, keyName='ErrorCount:Anylazer_items:%s' % parser_name.replace('Parser_', ''))
            if errorCount >= settings.ERRORMAX_items:
                sendMsg('Analyzer.items - %s error num up to %s' % (parser_name, errorCount))
            logger.error('Analyzer-item-Failed: %s' % parser_name)
            break
        if 'pipeline_dbType' not in item.__dict__.keys() or item.pipeline_dbType not in settings_temp.keys():
            logger.error('Please set \'pipeline_dbType\' in %s' % parser_name)
            continue
        queue_seed.setZero(keyName='ErrorCount:Analyzer_items:%s' % parser_name.replace('Parser_', ''))
        queue_seed.incr(1, keyName='Sum:Analyzer_items:%s' % parser_name.replace('Parser_', ''))
        dbType = item.pipeline_dbType
        settings_db = settings_temp.get(dbType, {})
        if parser_name not in DBS.keys():
            DBS[parser_name] = {}
        if dbType not in DBS[parser_name].keys():
            host = settings_db.get('host', 'localhost')
            port = settings_db.get('port', 0)
            db = item.__dict__.pop('pipeline_db') if 'pipeline_db' in item.__dict__.keys() else settings_db.get('db', 'default')
            account = settings_db.get('account')
            password = settings_db.get('password')
            DBS[parser_name][dbType] = queueFactory.create(dbType=QUEUES[dbType], host=host, port=port, db=db, account=account, password=password)
        try:
            keyName = item.__dict__.pop('pipeline_keyName') if 'pipeline_keyName' in item.__dict__.keys() else settings_db.get('keyName', 'default')
            collection = item.__dict__.pop('pipeline_collection') if 'pipeline_collection' in item.__dict__.keys() else settings_db.get('collection', 'default')
            index = item.__dict__.pop('pipeline_index') if 'pipeline_index' in item.__dict__.keys() else settings_db.get('index', 'default')
            doc_type = item.__dict__.pop('pipeline_doc_type') if 'pipeline_doc_type' in item.__dict__.keys() else settings_db.get('doc_type', 'default')
            if 'pipeline_method' in item.__dict__.keys():
                getattr(DBS[parser_name][dbType], item.__dict__.pop('pipeline_method'))(item.data, keyName=keyName, collection=collection, index=index, doc_type=doc_type)
            else:
                DBS[parser_name][dbType].put(item.data, keyName=keyName, collection=collection, index=index, doc_type=doc_type)
            num_items += 1
        except Exception as e:
            logger.error(e)
    return num_items


def pipeline_seeds(seeds, parser_name):
    """ 将解析出来的URL封装成种子，打入消息队列 """
    logger = logging.getLogger('root')
    num_crawled = 0
    num_seeds = 0
    for seed in seeds:
        try:
            if len(seed) == 0:
                errorCount = queue_seed.incr(1, keyName='ErrorCount:Anylazer_seeds:%s' % parser_name.replace('Parser_', ''))
                if errorCount >= settings.ERRORMAX_seeds:
                    sendMsg('Analyzer.seeds - %s error num up to %s' % (parser_name, errorCount))
                logger.error('Analyzer-seed-Failed: %s' % parser_name)
                break

            queue_seed.setZero(keyName='ErrorCount:Analyzer_seeds:%s' % parser_name.replace('Parser_', ''))
            queue_seed.incr(1, keyName='Sum:Analyzer_seeds:%s' % parser_name.replace('Parser_', ''))
            if 'spider' not in seed.keys():
                seed['spider'] = parser_name.replace('Parser', 'Spider')
            seed['time_parse'] = int(time.time())
            if 'dont_filter' in seed.keys() and seed['dont_filter']:
                try:
                    queue_seed.put(seed, keyName=settings.Queue_seed_keyName)
                    num_seeds += 1
                except Exception as e:
                    logger.error(e)
            elif not FILTER.isContains(seed['url']):  # 未爬则加入待爬队列
                FILTER.insert(seed['url'])  # 标志为已爬
                try:
                    queue_seed.put(seed, keyName=settings.Queue_seed_keyName)
                    num_seeds += 1
                except Exception as e:
                    logger.error(e)
            else:
                num_crawled += 1   # 已抓取的数量
                logger.debug('Existed: %s' % seed['url'])
        except Exception as e:
            logger.error(e)
    return num_seeds, num_crawled


def run(htmlNum, itemNum, seedNum):
    """ 每执行一次run()，解析一条HTML """
    logger = logging.getLogger('root')
    try:
        txt = queue_html.get(keyName=settings.Queue_html_keyName)
        html_packed = eval(txt[1] if isinstance(txt, tuple) else txt)  # 字符串转dict
    except Exception as e:
        logger.error('get html from redis error - %s' % str(e))
        return
    if html_packed:
        if '.' in html_packed['parser']:
            parser_name, method_name = html_packed['parser'].split('.')
        else:
            parser_name = html_packed['parser']
            method_name = 'parse0'
        parser = parserFactory.createObject(objectName=parser_name, url=html_packed['url'])
        method = parserFactory.createMethod(object=parser, methodName=method_name)
        if method is None:
            logger.warning('With no method: %s' % json.dumps(html_packed))
        else:
            try:
                items, seeds = method(html_packed)
            except Exception as e:
                logger.error('your parser error - %s' % str(e))
                return
            try:
                num_items = pipeline_items(items, parser_name)
                num_seeds, num_crawled = pipeline_seeds(seeds, parser_name)

                htmlNum.value += 1
                itemNum.value += num_items
                seedNum.value += num_seeds - num_crawled
                debug_msg = ('Source_url:%(url)s\nParser_name:%(parser)s\nNum_seeds:%(num_seeds)s(crawled:%(num_crawled)s)\nNum_items:%(num_items)s\n')
                debug_args = {'url': html_packed['url'], 'parser': parser_name, 'num_seeds': num_seeds, 'num_crawled': num_crawled, 'num_items': num_items}
                logger.debug(debug_msg, debug_args)
            except Exception as e:
                logger.error('deal parser result error - %s' % (str(e)))


def keep_log(htmls, items, seeds):
    """ 功能：INFO级别的日志监控，显示每分钟的抓取量 """
    logger = logging.getLogger('root')
    logger.warning('Now,We start:')
    htmlsprev = 0
    itemsprev = 0
    seedsprev = 0
    while True:
        speed_html = htmls.value - htmlsprev
        htmlsprev = htmls.value
        speed_item = items.value - itemsprev
        itemsprev = items.value
        speed_seed = seeds.value - seedsprev
        seedsprev = seeds.value
        msg = ('Parsed: %(num_htmls)s htmls( %(speed_html)s htmls/min)   Got: %(num_items)s items( %(speed_item)s items/min) 、 %(num_seeds)s seeds( %(speed_seed)s seeds/min)')
        log_args = {'num_htmls': htmls.value, 'speed_html': speed_html, 'num_items': items.value, 'speed_item': speed_item, 'num_seeds': seeds.value, 'speed_seed': speed_seed}
        logger.warning(msg, log_args)
        time.sleep(60)


def pre_run(htmls, items, seeds):
    """ 在每个进程里面再启动多协程 """
    logger = logging.getLogger('root')
    try:
        while True:  # 在此处循环而不在run里加循环的原因是：可以设置协程超时时间，回收死掉的协程
            threads = [gevent.spawn(run, htmls, items, seeds) for _ in range(settings.Num_gevent)]
            gevent.joinall(threads, timeout=settings.Timeout_gevent)
    except Exception as e:
        logger.error('One thread has downed!Reason:' + str(e))


def begin():
    """ 启动多进程 """
    plist = []
    htmls = sharedctypes.Value('l', 0, lock=False)
    items = sharedctypes.Value('l', 0, lock=False)
    seeds = sharedctypes.Value('l', 0, lock=False)
    p = Process(target=keep_log, args=(htmls, items, seeds))
    p.start()
    plist.append(p)
    for i in range(settings.Num_process):
        p = Process(target=pre_run, args=(htmls, items, seeds))
        p.start()
        plist.append(p)
    for p in plist:
        p.join()
