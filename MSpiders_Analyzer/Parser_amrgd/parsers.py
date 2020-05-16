# encoding=utf-8
# ---------------------------------------
#   语言：Python2.7
#   日期：
#   作者：
#   功能：amrgd爬虫解析规则
# ---------------------------------------

import logging
import re
import json
from lxml import etree

from common.models.model import Item
from common.parse.html_clean_tags import FilterTag
from common.parse.selector import Selector
from common.parse.utils import md5


class Parser_amrgd(object):
    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger('root')

    def parse0(self, html_packed):
        """
        seed键:
            'url'(必选): 待爬URL。
            'spider'(必选): 调用哪个下载规则, 格式为'Spider_amrgd.crawl1' 或 'Spider_amrgd'(默认使用crawl0方法)。
        field键:
            'pipeline_dbType'(必选): 数据库类型, 值为: mongo/es/redis/hbase/ssdb/mysql。
            'pipeline_keyName': 如果将数据存于Redis, 可带上此字段。如果没有带上则使用各爬虫settings.py中的keyName, 如果没有设置则默认使用'default'。
            'pipeline_collection': 如果将数据存于MongoDB, 可带上此字段。如果没有带上则使用各爬虫settings.py中的collection, 如果没有设置则默认使用'default'。
            'pipeline_index': 如果将数据存于ES, 可带上此字段, 如果没有带上则使用各爬虫settings.py中的index, 如果没有设置则默认使用'default'。
            'pipeline_doc_type': 如果将数据存于ES, 可带上此字段, 如果没有带上则使用各爬虫settings.py中的doc_type, 如果没有设置则默认使用'default'。
        """
        seeds = []
        fields = []
        try:
            selector = Selector(text=html_packed['html'].decode('utf-8', 'ignore'))
            data = {}
            url = html_packed['url']
            data['spider'] = '广东省市场监督管理局（知识产权局）'
            data['url'] = url
            data['type'] = '1'
            data['title'] = selector.xpath('//h1[@class="article_t"]/text()').extract()[0]
            data['source'] = selector.xpath('/html/body/div[4]/div[2]/div/div[1]/span[1]/text()').extract()[0]
            data['pushTime'] = selector.xpath('/html/body/div[4]/div[2]/div/div[1]/span[2]/text()').extract()[0].replace(
                "时间  :  ",
                '')[0:10]
            page = selector.xpath('//div[@class="article_con"]').extract()[0]
            files = []
            for at in selector.xpath('//div[@class="article_con"]//a'):
                file_url = at.xpath('@href').extract()[0]
                file_name = at.xpath('text()').extract()[0]
                file_type = file_url[-3:]
                file = {
                    'file_url': file_url,
                    'file_name': file_name,
                    'file_type': file_type
                }
                files.append(file)
            filters = FilterTag()
            content = filters.stripTagSimple(page)
            data['content'] = content
            data['len'] = len(content)
            data['page'] = page
            data['fid'] = md5(url)
            data['files'] = files
            item = Item(data=data, dbType='ffwb')
            fields.append(item)
        except Exception as e:
            self.logger.error(str(e))
        return fields, seeds

