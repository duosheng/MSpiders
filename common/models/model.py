# coding=utf-8

"""
        seed键:
            'url'(必选): 待爬URL。
            'spider'(必选): 调用哪个下载规则, 格式为'Spider_gdstc.crawl1' 或 'Spider_gdstc'(默认使用crawl0方法)。
        field键:
            'pipeline_dbType'(必选): 数据库类型, 值为: mongo/es/redis/hbase/ssdb/mysql。
            'pipeline_keyName': 如果将数据存于Redis, 可带上此字段。如果没有带上则使用各爬虫settings.py中的keyName, 如果没有设置则默认使用'default'。
            'pipeline_collection': 如果将数据存于MongoDB, 可带上此字段。如果没有带上则使用各爬虫settings.py中的collection, 如果没有设置则默认使用'default'。
            'pipeline_index': 如果将数据存于ES, 可带上此字段, 如果没有带上则使用各爬虫settings.py中的index, 如果没有设置则默认使用'default'。
            'pipeline_doc_type': 如果将数据存于ES, 可带上此字段, 如果没有带上则使用各爬虫settings.py中的doc_type, 如果没有设置则默认使用'default'。
"""


# 种子对象，里面包含一个需要下载的url，以及一个spider下载器
class Seed(object):

    def __init__(self, url, downloader):
        """
        :param url: 需要下载的url
        :param downloader: 需要哪个下载器，如果不传，使用默认下载器
        """
        self.url = url
        self.spider = downloader


# 结果对象，需要保存到db的数据
class Item(object):

    def __init__(self, data, dbType, keyName=None, collection=None, index=None, doc_type=None):
        self.data = data
        self.pipeline_dbType = dbType
        self.pipeline_keyName = keyName
        self.pipeline_collection = collection
        self.pipeline_index = index
        self.pipeline_doc_type = doc_type


"""
{'html': None, 'parser': 'Parser_gdstc.parse0'}
"""
class Html_packed(object):

    def __init__(self, html, parser):
        """
        :param html: 下载的html内容
        :param parser: 交给哪个解析器进行解析,如果不传，交给默认下载器
        """
        self.html = html
        self.parser = parser
