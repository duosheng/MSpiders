# encoding=utf-8
# ---------------------------------------
#   语言：Python2.7
#   日期：2017-07-10
#   作者：九茶<bone_ace@163.com>
#   功能：requests下载器
# ---------------------------------------
from urllib.parse import urlencode
import requests
import random
import logging
import redis
from MSpiders_Downloader import settings
from MSpiders_Downloader.Downloader.user_agents.user_agent import user_agents


class CrawlerRequests:
    def __init__(self):
        self.logger = logging.getLogger('root')
        self.rconn = redis.Redis(host=settings.Queue_seed_host, port=settings.Queue_seed_port, password=settings.Queue_seed_password)

    def visit(self, url, headers={}, data=None, cookie='', proxy=None, timeout=10, retry=1, isua=True, verify=False, **kwargs):
        if len(cookie) > 0:
            headers['Cookie'] = cookie
        if isua:
            headers['User-Agent'] = random.choice(user_agents)
        response = None
        failure = 0
        while retry >= failure:
            try:
                if data is not None:
                    response = requests.post(url, data=data, headers=headers, proxies=proxy, verify=verify, timeout=timeout)
                else:
                    response = requests.get(url, headers=headers, proxies=proxy, verify=verify, timeout=timeout)
                break
            except Exception as e:
                failure += 1
                try:
                    self.logger.error('open exception: %s' % str(e).decode('utf8', 'ignore').encode('unicode_escape'))
                except Exception as e:
                    self.logger.error('%s open exception' % url)
        if response is None:
            return None
        return {'content': response.content, 'status_code': response.status_code, 'cookie': urlencode(response.cookies.get_dict())}
