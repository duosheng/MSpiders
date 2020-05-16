# encoding=utf-8
# ---------------------------------------
#   语言：Python2.7
#   日期：2017-07-10
#   作者：九茶<bone_ace@163.com>
#   功能：数据于SSDB中存取
# ---------------------------------------


from ssdb.connection import BlockingConnectionPool
from ssdb import SSDB
import json

from common import QueueBase


class Queue_SSDB(QueueBase.QueueBase):
    def __init__(self, host='localhost', port=8888, **kwargs):
        QueueBase.QueueBase.__init__(self, host, port)
        self.__conn = SSDB(connection_pool=BlockingConnectionPool(host=self.host, port=self.port))
        self.name = kwargs.get('keyName', 'default')

    @QueueBase.catch
    def put(self, value, *args, **kwargs):
        return self.__conn.qpush_back(self.name, json.dumps(value) if isinstance(value, dict) or isinstance(value, list) else value)

    @QueueBase.catch
    def get(self, *args, **kwargs):
        value = self.__conn.qpop_front(self.name)
        return value[0] if value else value

    @QueueBase.catch
    def size(self, *args, **kwargs):
        return self.__conn.qsize(self.name)
