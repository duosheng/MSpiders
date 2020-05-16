# encoding=utf-8
# ---------------------------------------
#   语言：Python2.7
#   日期：
#   作者：
#   功能：bbsp2peye爬虫下载规则
# ---------------------------------------

import time
from MSpiders_Downloader.settings import Spider_bbsp2peye as settings
from MSpiders_Downloader.Downloader.utils.DingDingRobot import sendMsg
from MSpiders_Downloader.Downloader.proxies.methods import getOneProxy, putOneProxy
from MSpiders_Downloader.Downloader.crawlers.CrawlerRequests import CrawlerRequests


class Spider_bbsp2peye(CrawlerRequests):

    def crawl0(self, seed_packed):
        html_packed = {'html': None}
        for name in ['category', 'trytime', 'description', 'coverImg', 'pubTime', 'readCount', 'commentCount', 'start', 'end']:
            if name in seed_packed.keys():
                html_packed[name] = seed_packed[name]

        failure = 0
        while failure < 3:
            time.sleep(settings.get('DELAY', 2))
            proxy = getOneProxy(keyName='Proxies:bbsp2peye', obj=self) if settings.get('ISPROXY', False) else None
            if '/forum' in seed_packed['url']:
                response = self.visit(seed_packed['url'], proxy=proxy, headers={'User-Agent': 'Mozilla/5.0 (Linux; U; Android 1.5; fr-fr; GT-I5700 Build/CUPCAKE) AppleWebKit/528.5 (KHTML, like Gecko) '}, isua=False, retry=settings.get('RETRY', 2))
            else:
                response = self.visit(seed_packed['url'], proxy=proxy, retry=settings.get('RETRY', 2))

            if response is None:
                failure += 1
                continue
            elif response['status_code'] in [403, ]:
                self.logger.error('bbsp2peye 403 - %s' % seed_packed['url'])
                sendMsg('bbsp2peye 403 - %s' % seed_packed['url'])
            else:
                if proxy is not None:
                    putOneProxy(proxy=proxy, keyName='Proxies:bbsp2peye', obj=self)
                if response['status_code'] in [404, ]:
                    self.logger.warning('bbsp2peye %s - %s' % (response['status_code'], seed_packed['url']))
                    html_packed['html'] = ''        # 设为空字符串，将会忽略，不报警，不入failure队列
                else:
                    html_packed['html'] = response['content']
                    if '/ptdt' in seed_packed['url'] or '/wdzl' in seed_packed['url'] or '/wdxw' in seed_packed['url']:
                        html_packed['parser'] = 'Parser_bbsp2peye.parse0'
                    elif '/article' in seed_packed['url']:
                        html_packed['parser'] = 'Parser_bbsp2peye.parse1'
                    elif '/forum' in seed_packed['url']:
                        html_packed['parser'] = 'Parser_bbsp2peye.parse2'
                    elif '/thread' in seed_packed['url']:
                        html_packed['parser'] = 'Parser_bbsp2peye.parse3'
                    elif '/gfdt' in seed_packed['url']:
                        html_packed['parser'] = 'Parser_bbsp2peye.parse4'
            break
        return [html_packed, ]

