# encoding=utf-8
# ---------------------------------------
#   功能：爬虫监控调度任务
# ---------------------------------------
import sys
import time

import requests

from MSpiders_Analyzer.Analyzer.beginer import FILTER
from common.models.model import Seed
from common.parse.selector import Selector
from watch_dogs.utils import readTime, push_seed, writeLog


def job_bbsp2peye0():
    start, end = readTime(spiderName='bbsp2peye0')
    t1 = time.time()
    seeds = {
        'http://news.p2peye.com/ptdt/': '平台动态',
        'http://news.p2peye.com/wdzl/': '网贷专栏',
        'http://news.p2peye.com/wdxw/': '网贷新闻',
        'http://www.p2peye.com/forum-60-1.html': '曝光台',
    }
    for seed in seeds.keys():
        try:
            data = {
                'url': seed,
                'spider': 'Spider_bbsp2peye',
                'category': seeds[seed],
                'start': start,
                'end': end,
            }
            push_seed(data)
        except Exception as e:
            writeLog(str(e))
    writeLog('Finish add the seeds of bbsp2peye0 (Used: %s)' % (time.time() - t1))





def job_gdstc():

    # 文章列表页
    urls = []
    for i in range(1, 21):
        if (i == 1):
            url = "http://gdstc.gd.gov.cn/zwgk_n/tzgg/index.html"
        else:
            url = "http://gdstc.gd.gov.cn/zwgk_n/tzgg/index_%s.html" % str(i)
        urls.append(url)

    # 文章详情页
    for url in urls:
        t1 = time.time()
        headers = {
            'Accept-Encoding': "gzip, deflate",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Upgrade-Insecure-Requests': "1",
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36",
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            'Referer': "http://gdstc.gd.gov.cn/zwgk_n/",
            'Cookie': "zh_choose=s; zh_choose=s; openstack_cookie_insert=76667651",
            'Connection': "keep-alive"
        }
        response = requests.request("GET", url, headers=headers)
        selector = Selector(text=response.text)
        urls = selector.xpath("/html/body/div[2]/div[2]/div[2]/ul/li/a/@href").extract()
        for u in urls:
            if not FILTER.isContains(u):   # 如果还没有爬过
                FILTER.insert(u)           # 标志为已爬
                seed = Seed(url=u, downloader='gdstc.crawl0')
                push_seed(seed)
            # seed = Seed(url=u, downloader='gdstc.crawl0')
            # push_seed(seed)
        writeLog('Finish add the seeds of gdstc (Used: %s)' % (time.time() - t1))


def job_scjgjjs():

    # 文章列表页
    urls = []
    for i in range(1, 21):
        if (i == 1):
            url = "http://scjgj.jiangsu.gov.cn/col/col70311/index.html"
        else:
            url = "http://scjgj.jiangsu.gov.cn/col/col70311/index.html?uid=277431&pageNum=%s" % str(i)
        urls.append(url)

    # 文章详情页
    for url in urls:
        t1 = time.time()
        headers = {
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Referer': 'http://test.gzjirui.com/magicflu/html/form/records2.jsp?spaceId=02393294-327d-43ed-835e-d8fe778772a8&formId=-1',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cookie': '__jsluid_h=8011b3a4cb561d1de121a1fa390ab4df; _gscu_1226760719=8861650310idmp17; _gscbrs_1226760719=1; yunsuo_session_verify=75a060942bec9e14902b3b5453719ad1; _gscs_1226760719=t89123468mg3q2f70|pv:3'
        }
        response = requests.request("GET", url, headers=headers)
        selector = Selector(text=response.text)
        urls = selector.xpath('//*[@id="277431"]/div/li[1]/a/@href').extract()
        for u in urls:
            if not FILTER.isContains(u):   # 如果还没有爬过
                FILTER.insert(u)           # 标志为已爬
                seed = Seed(url=u, downloader='gdstc.crawl0')
                push_seed(seed)
            # seed = Seed(url=u, downloader='gdstc.crawl0')
            # push_seed(seed)
        writeLog('Finish add the seeds of gdstc (Used: %s)' % (time.time() - t1))



def job_amrgd():

    # 文章列表页
    urls = []
    for i in range(1, 21):
        if (i == 1):
            url = "http://amr.gd.gov.cn/zwgk/tzgg/index.html"
        else:
            url = "http://amr.gd.gov.cn/zwgk/tzgg/index_%s.html" % str(i)
        urls.append(url)

    # 文章详情页
    for url in urls:
        t1 = time.time()
        headers = {
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Referer': 'http://amr.gd.gov.cn/zwgk/tzgg/index.html',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        response = requests.request("GET", url, headers=headers)
        selector = Selector(text=response.text)
        urls = selector.xpath("/html/body/div[4]/div[2]/div[2]/div/ul/li[1]/h3/a/@href").extract()
        for u in urls:
            if not FILTER.isContains(u):   # 如果还没有爬过
                FILTER.insert(u)           # 标志为已爬
                seed = Seed(url=u, downloader='amrgd.crawl0')
                push_seed(seed)
            # seed = Seed(url=u, downloader='amrgd.crawl0')
            # push_seed(seed)
        writeLog('Finish add the seeds of amrgd (Used: %s)' % (time.time() - t1))


def job_nrgd():

    # 文章列表页
    urls = []
    for i in range(1, 20):
        if (i == 1):
            url = "http://nr.gd.gov.cn/zwgknew/tzgg/index.html"
        else:
            url = "http://nr.gd.gov.cn/zwgknew/tzgg/index_%s.html" % str(i)
        urls.append(url)

    # 文章详情页
    for url in urls:
        t1 = time.time()
        headers = {
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Referer': 'http://nr.gd.gov.cn/zwgknew/tzgg/index.html',
            'Accept-Language': 'zh-CN,zh;q=0.9'
        }
        response = requests.request("GET", url, headers=headers)
        selector = Selector(text=response.text)
        urls = selector.xpath("/html/body/div[2]/div[2]/div[2]/ul/li[3]/a/@href").extract()
        for u in urls:
            if not FILTER.isContains(u):   # 如果还没有爬过
                FILTER.insert(u)           # 标志为已爬
                seed = Seed(url=u, downloader='nrgd.crawl0')
                push_seed(seed)
            # seed = Seed(url=u, downloader='nrgd.crawl0')
            # push_seed(seed)
        writeLog('Finish add the seeds of nrgd (Used: %s)' % (time.time() - t1))


def job_gdeegd():

    # 文章列表页
    urls = []
    for i in range(1, 64):
        if (i == 1):
            url = "http://gdee.gd.gov.cn/ggtz3126/index.html"
        else:
            url = "http://gdee.gd.gov.cn/ggtz3126/index_%s.html" % str(i)
        urls.append(url)

    # 文章详情页
    for url in urls:
        t1 = time.time()
        headers = {
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Referer': 'http://gdee.gd.gov.cn/ggtz3126/index_3.html',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cookie': 'm_bt=yes; openstack_cookie_insert=62355311; _gscu_1815356153=89127015q6kzl720; _gscbrs_1815356153=1; UM_distinctid=171ff59ebaa814-0ab1f7a365db41-d373666-1fa400-171ff59ebab197; CNZZDATA3588456=cnzz_eid%3D214537553-1589123201-http%253A%252F%252Ftest.gzjirui.com%252F%26ntime%3D1589123201; _gscs_1815356153=89127015ev2u6d20|pv:2'
        }
        response = requests.request("GET", url, headers=headers)
        selector = Selector(text=response.text)
        urls = selector.xpath("/html/body/div/div[3]/div[2]/div/div[2]/ul/li[3]/div/a/@href").extract()
        for u in urls:
            if not FILTER.isContains(u):   # 如果还没有爬过
                FILTER.insert(u)           # 标志为已爬
                seed = Seed(url=u, downloader='gdeegd.crawl0')
                push_seed(seed)
            # seed = Seed(url=u, downloader='gdeegd.crawl0')
            # push_seed(seed)
        writeLog('Finish add the seeds of gdeegd (Used: %s)' % (time.time() - t1))


def job_comgdgov():

    # 文章列表页
    urls = []
    for i in range(1, 16):
        if (i == 1):
            url = "http://com.gd.gov.cn/zwgk/gggs/index.html"
        else:
            url = "http://com.gd.gov.cn/zwgk/gggs/index_%s.html" % str(i)
        urls.append(url)

    # 文章详情页
    for url in urls:
        t1 = time.time()
        headers = {
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Referer': 'http://com.gd.gov.cn/zwgk/gggs/index_16.html',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cookie': 'UM_distinctid=171ff59ebaa814-0ab1f7a365db41-d373666-1fa400-171ff59ebab197; openstack_cookie_insert=81202878'
        }
        response = requests.request("GET", url, headers=headers)
        selector = Selector(text=response.text)
        urls = selector.xpath("/html/body/div[2]/div/div[2]/ul/li[4]/a/@href").extract()
        for u in urls:
            if not FILTER.isContains(u):   # 如果还没有爬过
                FILTER.insert(u)           # 标志为已爬
                seed = Seed(url=u, downloader='comgdgov.crawl0')
                push_seed(seed)
            # seed = Seed(url=u, downloader='comgdgov.crawl0')
            # push_seed(seed)
        writeLog('Finish add the seeds of comgdgov (Used: %s)' % (time.time() - t1))


if __name__ == '__main__':
    # job_comgdgov()
    sys.argv
    if len(sys.argv) == 1:
        print('you must set the parameters for spider name')
        sys.exit()
    spider_name = sys.argv[1]
    eval('job_%s' % spider_name)()

