# coding=utf-8

import requests

from common.parse.html_clean_tags import FilterTag
from common.parse.selector import Selector
from common.queues.ffwb import FFWBAPI
import hashlib
import html

def md5(str):
    return hashlib.md5(str.encode('utf-8')).hexdigest()




def crawle(url):
    headers = {
        'Accept-Encoding': "gzip, deflate",
        'Accept-Language': "zh-CN,zh;q=0.9",
        'Upgrade-Insecure-Requests': "1",
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'Referer': "http://gdstc.gd.gov.cn/zwgk_n/",
        'Cookie': "zh_choose=s; zh_choose=s; openstack_cookie_insert=76667651",
        'Connection': "keep-alive",
        'Cache-Control': "no-cache",
        'Postman-Token': "480ed1c9-c418-4670-9e85-40a1063dae87"
    }
    response = requests.request("GET", url, headers=headers)
    selector = Selector(text=response.text)
    data = {}
    data['url'] = url
    data['type'] = '1'
    data['title'] = selector.xpath('//h3[@class="zw-title"]/text()').extract()[0]
    data['source'] = selector.xpath('//span[@class="ly"]/text()').extract()[0].replace("来源  :  ", '')
    data['pushTime'] = selector.xpath('/html/body/div[2]/div[2]/div[2]/span[1]/text()').extract()[0].replace("时间  :  ",
                                                                                                             '')[0:10]
    page = selector.xpath('//div[@class="zw"]').extract()[0]
    files = []
    for at in selector.xpath('//div[@class="zw"]//a'):
        file_url = at.xpath('@href').extract()[0]
        file_name = at.xpath('text()').extract()[0]
        file_type = file_url[-3:]
        # 下载附件
        down_res = requests.get(url=file_url, headers=headers)
        file_path = 'D:\\data\\files\\%s.%s' % (file_name, file_type)
        with open(file_path, "wb") as code:
            code.write(down_res.content)
        files.append(file_path)
    filters = FilterTag()
    content = filters.stripTagSimple(page)
    data['content'] = content
    data['len'] = len(content)
    data['page'] = page
    data['fid'] = md5(url)
    try:
        space_id = "93d0b958-52d3-4858-b6e9-344a23aede67"
        table_id = "2717074e-7886-4495-9a0e-4733e55098d2"
        ffwbapi = FFWBAPI(space_id=space_id, table_id=table_id)
        ffwbapi.insert_record(data=data)
        id = ffwbapi.get_id(fid=data['fid'])
        for f in files:
                ffwbapi.upload_file(id=id, file_path=f)
    except Exception as e:
        print(e)

def gdstc(url):
    headers = {
        'Accept-Encoding': "gzip, deflate",
        'Accept-Language': "zh-CN,zh;q=0.9",
        'Upgrade-Insecure-Requests': "1",
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'Referer': "http://gdstc.gd.gov.cn/zwgk_n/",
        'Cookie': "zh_choose=s; zh_choose=s; openstack_cookie_insert=76667651",
        'Connection': "keep-alive",
        'Cache-Control': "no-cache",
        'Postman-Token': "1cae4a74-ceb5-04d1-1fe9-3df1fe66edf3"
    }
    response = requests.request("GET", url, headers=headers)
    selector = Selector(text=response.text)
    urls = selector.xpath("/html/body/div[2]/div[2]/div[2]/ul/li/a/@href").extract()
    for url in urls:
        try:
            crawle(url)
        except Exception as e:
            pass


if __name__ == '__main__':
    urls = []
    for i in range(1, 21):
        if (i==1):
            url = "http://gdstc.gd.gov.cn/zwgk_n/tzgg/index.html"
        else:
            url = "http://gdstc.gd.gov.cn/zwgk_n/tzgg/index_%s.html" % str(i)
        urls.append(url)

    for u in urls:
        print(u)
        gdstc(u)

    # crawle('http://gdstc.gd.gov.cn/zwgk_n/tzgg/content/post_2971267.html')


