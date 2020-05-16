# encoding=utf-8
# ---------------------------------------
#   语言：Python2.7
#   日期：2017-07-10
#   作者：code pande
#   功能：urllib2下载器
# ---------------------------------------


import gzip
import time
from io import StringIO
import urllib.request as urllib2
import urllib
import random
import logging
from MSpiders_Downloader.Downloader.user_agents.user_agent import user_agents


class CrawlerUrllib2:
    def __init__(self):
        self.logger = logging.getLogger('root')

    def visit(self, url, headers={}, data=None, cookie='', proxy=None, timeout=20, retry=1, isua=True, **kwargs):
        req = urllib2.Request(url, data=urllib.urlencode(data) if isinstance(data, dict) else data, headers=headers)
        handlers = list()
        if isua:
            req.add_header('User-Agent', random.choice(user_agents))
        if proxy is not None:
            handlers.append(urllib2.ProxyHandler(proxy))
        if len(cookie) > 0:
            handlers.append(urllib2.HTTPCookieProcessor(cookie))
        opener = urllib2.build_opener(*handlers)
        response = None
        failure = 0
        while retry >= failure:
            failure += 1
            try:
                response = opener.open(req, timeout=timeout)
                break
            except Exception as e:
                try:
                    self.logger.error('%s open exception: %s' % (url, str(e).decode('utf8', 'ignore').encode('unicode_escape')))
                except Exception as e:
                    self.logger.error('%s open exception' % url)
                time.sleep(2)
        if not response:
            opener.close()
            return None
        try:
            if response.info().get('Content-Encoding') == 'gzip':
                result = gzip.GzipFile(fileobj=StringIO.StringIO(response.read())).read()
            else:
                result = response.read()
        except Exception as e:
            try:
                self.logger.error('decode gzip exception: %s' % str(e))
            except Exception as e:
                self.logger.error('decode gzip exception')
            response.close()
            opener.close()
            return None
        response.close()
        opener.close()
        return {'content': result, 'status_code': response.code}
