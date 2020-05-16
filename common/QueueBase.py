# encoding=utf-8
# ---------------------------------------
#   语言：Python2.7
#   日期：2017-07-10
#   作者：九茶<bone_ace@163.com>
#   功能：数据队列的基类
# ---------------------------------------


import logging
from abc import ABCMeta, abstractmethod


logger = logging.getLogger('root')


def catch(func):
    def decorator(*args, **kwargs):
        failure = 0
        while failure < 2:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error('queue error - %s' % str(e))
                if 'ProduceResponse' in str(e):
                    return
                if '\'utf8\' codec can\'t decode byte' in str(e):
                    return
                if 'E11000' in str(e):
                    return
                failure += 1

    return decorator


class QueueBase(object):
    __metaclass__ = ABCMeta

    def __init__(self, host, port):
        self.host = host
        self.port = port

    @abstractmethod
    def put(self, value, *args, **kwargs):
        pass

    @abstractmethod
    def get(self, *args, **kwargs):
        pass

    @abstractmethod
    def size(self, *args, **kwargs):
        pass
