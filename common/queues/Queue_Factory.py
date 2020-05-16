# encoding=utf-8
# ---------------------------------------
#   语言：Python2.7
#   日期：2017-07-10
#   作者：code pande
#   功能：数据队列工厂
# ---------------------------------------


import importlib


class QueueFactory(object):
    def create(self, dbType, host, port, **kwargs):
        return getattr(importlib.import_module('common.queues.' + dbType), dbType)(host=host, port=port, **kwargs)
