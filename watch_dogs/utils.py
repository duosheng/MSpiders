# encoding=utf-8
# ---------------------------------------
#   语言：Python2.7
#   日期：
#   作者：
#   功能：爬虫监控调度
# ---------------------------------------

import datetime
import json

import pymongo
import redis
import requests

from watch_dogs import settings

# CLIENT = pymongo.MongoClient(host=settings.MONGO_HOST, port=settings.MONGO_PORT)
# DB_STOCK = CLIENT['fund']
# if len(settings.MONGO_USER) > 0:
#     DB_STOCK.authenticate(name=settings.MONGO_USER, password=settings.MONGO_PASS)
RCONN = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB,
                    password=settings.REDIS_PASSWORD)

def push_seed(seed):
    """
    将seed放入队列
    :param data:
    :return:
    """
    RCONN.lpush(settings.REDIS_KEYNAME, json.dumps(seed.__dict__))

def sendMsg(txt):
    try:
        data = {"msgtype": "text", "text": {"content": txt}, "at": {"isAtAll": False}}
        requests.post(settings.DingDingNoticeUrl, data=json.dumps(data), headers={"Content-type": "application/json"})
    except Exception as e:
        pass


def writeLog(txt):
    date_str = datetime.datetime.now().strftime('%Y-%m-%d')
    with open(settings.WatchDog_LOGPATH + 'log.{}'.format(date_str), 'a') as f:
        f.write('%s: %s\n' % (datetime.datetime.now(), txt))
    print('%s: %s' % (datetime.datetime.now(), txt))


def readTime(spiderName, sep='-'):
    end = datetime.datetime.now().strftime('%Y' + sep + '%m' + sep + '%d %H:%M:%S')
    start = '1970%s01%s01 08:00:00' % (sep, sep)
    if 'Timetable:%s' % spiderName in RCONN.keys('Timetable*'):
        txt = RCONN.lrange('Timetable:%s' % spiderName, 0, 0)
        if len(txt) > 0 and len(txt[0].strip()):
            start = txt[0].strip()
    RCONN.lpush('Timetable:%s' % spiderName, end)
    return start, end


def cleanProxies(txt=''):
    if RCONN.llen('Proxies:%s' % txt) > 0:
        RCONN.delete('Proxies:%s' % txt)


def crawlContent(url, headers={}, data=None):
    failure = 0
    while failure < 3:
        try:
            if data is None:
                r = requests.get(url, headers=headers)
            else:
                r = requests.post(url, data=data, headers=headers)
            return r.content
        except Exception as e:
            failure += 1


