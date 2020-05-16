# encoding=utf-8
# ---------------------------------------
#   语言：Python2.7
#   日期：2017-07-10
#   作者：code pande
#   功能：数据于ES中存取
# ---------------------------------------


import uuid
import elasticsearch

from common import QueueBase


class Queue_ElasticSearch(QueueBase.QueueBase):
    def __init__(self, host='localhost', port=9200, **kwargs):
        QueueBase.QueueBase.__init__(self, host, port)
        self.__conn = elasticsearch.Elasticsearch(hosts=':'.join([self.host, str(self.port)]))

    @QueueBase.catch
    def put(self, value, *args, **kwargs):
        if kwargs.has_key('index') and kwargs.has_key('doc_type'):
            esID = value.pop('_id') if '_id' in value.keys() else str(uuid.uuid1())
            return self.__conn.index(index=kwargs.get('index'), doc_type=kwargs.get('doc_type'), id=esID, body=value)

    @QueueBase.catch
    def get(self, *args, **kwargs):
        if kwargs.has_key('_id') and kwargs.has_key('index') and kwargs.has_key('doc_type'):
            return self.__conn.search(index=kwargs.get('index'), doc_type=kwargs.get('doc_type'), id=kwargs.get('_id'))

    @QueueBase.catch
    def size(self, *args, **kwargs):
        return self.__conn.count()
