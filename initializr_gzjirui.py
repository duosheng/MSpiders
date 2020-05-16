# encoding=utf-8

import os
import sys
import getopt


def create(name):
    filenames = os.listdir('MSpiders_Analyzer') + os.listdir('MSpiders_Downloader')
    if 'Parser_%s' % name in filenames or 'Spider_%s' % name in filenames:
        print('This name is not allowed! (Existed!)')
        return

    # 新建文件夹
    os.mkdir('MSpiders_Analyzer/Parser_%s' % name)
    os.mkdir('MSpiders_Downloader/Spider_%s' % name)

    # 新建文件
    with open('MSpiders_Analyzer/Parser_%s/__init__.py' % name, 'w') as f:
        pass

    with open('MSpiders_Analyzer/Parser_%s/parsers.py' % name, 'w') as f:
        txt = """# encoding=utf-8
# ---------------------------------------
#   语言：Python2.7
#   日期：
#   作者：
#   功能：%s爬虫解析规则
# ---------------------------------------

import logging
import re
import json
from lxml import etree

from common.models.model import Item
from common.parse.html_clean_tags import FilterTag
from common.parse.selector import Selector
from common.parse.utils import md5


class Parser_%s(object):
    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger('root')

    def parse0(self, html_packed):
        \"""
        seed键:
            'url'(必选): 待爬URL。
            'spider'(必选): 调用哪个下载规则, 格式为'Spider_%s.crawl1' 或 'Spider_%s'(默认使用crawl0方法)。
        field键:
            'pipeline_dbType'(必选): 数据库类型, 值为: mongo/es/redis/hbase/ssdb/mysql。
            'pipeline_keyName': 如果将数据存于Redis, 可带上此字段。如果没有带上则使用各爬虫settings.py中的keyName, 如果没有设置则默认使用'default'。
            'pipeline_collection': 如果将数据存于MongoDB, 可带上此字段。如果没有带上则使用各爬虫settings.py中的collection, 如果没有设置则默认使用'default'。
            'pipeline_index': 如果将数据存于ES, 可带上此字段, 如果没有带上则使用各爬虫settings.py中的index, 如果没有设置则默认使用'default'。
            'pipeline_doc_type': 如果将数据存于ES, 可带上此字段, 如果没有带上则使用各爬虫settings.py中的doc_type, 如果没有设置则默认使用'default'。
        \"""
        seeds = []
        fields = []
        try:
            selector = Selector(text=html_packed['html'].decode('utf-8', 'ignore'))
            data = {}
            url = html_packed['url']
            data['spider'] = '广东省科学技术厅'
            data['url'] = url
            data['type'] = '1'
            data['title'] = selector.xpath('//h3[@class="zw-title"]/text()').extract()[0]
            data['source'] = selector.xpath('//span[@class="ly"]/text()').extract()[0].replace("来源  :  ", '')
            data['pushTime'] = selector.xpath('/html/body/div[2]/div[2]/div[2]/span[1]/text()').extract()[0].replace(
                "时间  :  ",
                '')[0:10]
            page = selector.xpath('//div[@class="zw"]').extract()[0]
            files = []
            for at in selector.xpath('//div[@class="zw"]//a'):
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

""" % tuple([name]*4)
        f.write(txt)

    with open('MSpiders_Downloader/Spider_%s/__init__.py' % name, 'w') as f:
        pass

    with open('MSpiders_Downloader/Spider_%s/spiders.py' % name, 'w') as f:
        txt = """# encoding=utf-8
# ---------------------------------------
#   语言：Python2.7
#   日期：
#   作者：
#   功能：%s爬虫下载规则
# ---------------------------------------

import time
from MSpiders_Downloader.settings import Spider_%s as settings
from MSpiders_Downloader.Downloader.proxies.methods import getOneProxy, putOneProxy
from MSpiders_Downloader.Downloader.crawlers.CrawlerRequests import CrawlerRequests


class Spider_%s(CrawlerRequests):

    def crawl0(self, seed_packed):
        \"""
        html_packed键:
            'parser'(必选): 调用哪个解析规则, 格式为'Parser_%s.parse1' 或 'Parser_%s'(默认使用parse0方法)。
            'html'(必选): 待解析的HTML。
        \"""
        html_packed = {'html': None, 'parser': 'Parser_%s.parse0'}
        failure = 0
        while failure < 3:
            time.sleep(settings.get('DELAY', 2))
            proxy = getOneProxy(keyName='Proxies:%s', obj=self) if settings.get('ISPROXY', False) else None
            response = self.visit(seed_packed['url'], proxy=proxy, retry=settings.get('RETRY', 2))
            if response is None:
                failure += 1
            elif response['status_code'] not in [403, ]:
                if proxy is not None:
                    putOneProxy(proxy=proxy, keyName='Proxies:%s', obj=self)
                html_packed['html'] = response['content']
                break

        return [html_packed, ]


""" % tuple([name]*8)
        f.write(txt)


if __name__ == '__main__':
    txt = sys.argv[1:]
    # txt = ['Demo1']
    if len(txt) == 0:
        print('you need to type the name of the spider.(Such like: "python initializr.py Demo")')
    else:
        create(name=txt[0])
        print('Finish!')



