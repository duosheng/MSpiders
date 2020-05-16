# encoding=utf-8

import time


def getOneProxy(keyName, obj):
    while obj.rconn.llen(keyName) < 3:
        obj.logger.warning('%s need proxies, waiting...' % keyName)
        time.sleep(10)
    proxy = eval(obj.rconn.rpop(keyName))
    return proxy


def putOneProxy(proxy, keyName, obj):
    obj.rconn.lpush(keyName, str(proxy))
