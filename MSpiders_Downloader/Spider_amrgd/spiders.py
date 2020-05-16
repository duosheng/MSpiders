# encoding=utf-8
# ---------------------------------------
#   语言：Python2.7
#   日期：
#   作者：
#   功能：amrgd爬虫下载规则
# ---------------------------------------

import time
from MSpiders_Downloader.settings import Spider_amrgd as settings
from MSpiders_Downloader.Downloader.proxies.methods import getOneProxy, putOneProxy
from MSpiders_Downloader.Downloader.crawlers.CrawlerRequests import CrawlerRequests


class Spider_amrgd(CrawlerRequests):

    def crawl0(self, seed_packed):
        """
        html_packed键:
            'parser'(必选): 调用哪个解析规则, 格式为'Parser_amrgd.parse1' 或 'Parser_amrgd'(默认使用parse0方法)。
            'html'(必选): 待解析的HTML。
        """
        html_packed = {'html': None, 'parser': 'Parser_amrgd.parse0'}
        failure = 0
        while failure < 3:
            time.sleep(settings.get('DELAY', 2))
            proxy = getOneProxy(keyName='Proxies:amrgd', obj=self) if settings.get('ISPROXY', False) else None
            response = self.visit(seed_packed['url'], proxy=proxy, retry=settings.get('RETRY', 2))
            if response is None:
                failure += 1
            elif response['status_code'] not in [403, ]:
                if proxy is not None:
                    putOneProxy(proxy=proxy, keyName='Proxies:amrgd', obj=self)
                html_packed['html'] = response['content']
                break

        return [html_packed, ]


