# encoding=utf-8
# ---------------------------------------
#   语言：Python2.7
#   日期：2017-07-10
#   作者：code pande
#   功能：数据于MongoDB中存取
# ---------------------------------------


import pymongo

from common import QueueBase


class Queue_MongoDB(QueueBase.QueueBase):
    def __init__(self, host='localhost', port=27017, **kwargs):
        QueueBase.QueueBase.__init__(self, host, port)
        self.client = pymongo.MongoClient(host=self.host, port=self.port)
        self.db = self.client[kwargs.get('db', 'default')]
        if kwargs.get('account') and kwargs.get('password'):
            self.db.authenticate(kwargs.get('account'), kwargs.get('password'))

    @QueueBase.catch
    def put(self, value, *args, **kwargs):
        if 'collection' in kwargs:
            return self.db[kwargs.get('collection')].insert(value)

    @QueueBase.catch
    def get(self, *args, **kwargs):
        if 'collection' in kwargs:
            return self.db[kwargs.get('collection')].find_one_and_delete()

    @QueueBase.catch
    def update(self, value, *args, **kwargs):
        if 'collection' in kwargs:
            return self.db[kwargs.get('collection')].save(value)

    @QueueBase.catch
    def size(self, *args, **kwargs):
        if 'collection' in kwargs:
            return self.db[kwargs.get('collection')].count()
