# encoding=utf-8
# ---------------------------------------
#   语言：Python2.7
#   日期：2017-07-10
#   作者：code pande
#   功能：数据于Redis的list中存取
# ---------------------------------------


import redis

from common import QueueBase


class Queue_Redis(QueueBase.QueueBase):
    def __init__(self, host='localhost', port=6379, **kwargs):
        QueueBase.QueueBase.__init__(self, host, port)
        self.__conn = redis.Redis(host=self.host, port=self.port, db=kwargs.get('db', 0), password=kwargs.get('password', None))

    @QueueBase.catch
    def put(self, value, *args, **kwargs):
        if 'keyName' in kwargs:
            return self.__conn.rpush(kwargs.get('keyName'), str(value) if isinstance(value, dict) or isinstance(value, list) else value)

    @QueueBase.catch
    def get(self, *args, **kwargs):
        if 'keyName' in kwargs:
            return self.__conn.blpop(kwargs.get('keyName'))

    @QueueBase.catch
    def size(self, *args, **kwargs):
        if 'keyName' in kwargs:
            return self.__conn.llen(kwargs.get('keyName'))

    @QueueBase.catch
    def incr(self, value, *args, **kwargs):
        if 'keyName' in kwargs:
            return self.__conn.incr(kwargs.get('keyName'), value)

    @QueueBase.catch
    def setZero(self, *args, **kwargs):
        if 'keyName' in kwargs:
            return self.__conn.set(kwargs.get('keyName'), 0)
