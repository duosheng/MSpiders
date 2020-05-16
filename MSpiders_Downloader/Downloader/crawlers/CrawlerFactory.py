# encoding=utf-8
# ---------------------------------------
#   语言：Python2.7
#   日期：2017-07-10
#   作者：code pande
#   功能：下载规则工厂
# ---------------------------------------


import importlib


class CrawlerFactory(object):
    def createObject(self, objectName, *args, **kwargs):
        if len(objectName) > 0:
            return getattr(importlib.import_module('MSpiders_Downloader.Spider_%s.spiders' % objectName), 'Spider_%s' % objectName)(*args, **kwargs)

    def createMethod(self, methodName, object='', *args, **kwargs):
        if object is not None:
            return getattr(object, methodName)
