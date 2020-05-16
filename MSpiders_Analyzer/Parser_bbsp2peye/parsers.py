# encoding=utf-8
# ---------------------------------------
#   语言：Python2.7
#   日期：
#   作者：
#   功能：bbsp2peye爬虫解析规则
# ---------------------------------------

import logging
import time
import re
import json
from xml import etree

from ..items.item import ArticleItem, CommentItem


class Parser_bbsp2peye(object):
    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger('root')

    def parse0(self, html_packed):
        """ 网贷新闻、平台动态、网贷专栏 """
        seeds = []
        try:
            tree = etree.HTML(html_packed['html'].decode('gbk', 'ignore'))
            txt = 'listbox20' if html_packed['category'] == '网贷新闻' else ('listbox28' if html_packed['category'] == '平台动态' else 'listbox26')
            divs = tree.xpath('//div[@id="%s"]//div[@class="mod-leftfixed mod-news clearfix"]' % txt)
            for div in divs:
                try:
                    seed = {'spider': 'Spider_bbsp2peye.crawl0', 'category': html_packed['category'], 'pubTime': time.strftime('%Y-%m-%d %H:%M', time.localtime())}
                    # URL
                    url = div.xpath('.//div[@class="main"]//div[@class="hd"]/a/@href')
                    if len(url) == 0:
                        url = div.xpath('.//div[@class="sub"]/div[@class="inner"]/a/@href')
                    if len(url) > 0:
                        seed['url'] = url[0]

                        # 描述
                        description = ' '.join(div.xpath('.//div[@class="main"]//div[@class="bd"]//text()')).strip()
                        if len(description) > 0:
                            seed['description'] = description

                        # 封面图片
                        coverImg = div.xpath('.//div[@class="sub"]/div[@class="inner"]/a/img[@class="tn"]/@src')
                        if len(coverImg) > 0:
                            seed['coverImg'] = coverImg[0]

                        # 发表时间
                        pubTime = div.xpath('.//div[@class="main"]//div[@class="fd-left"]//span')
                        if len(pubTime) > 0:
                            pubTime = pubTime[-1].xpath('./text()')
                            if len(pubTime) > 0 and pubTime[0].strip().startswith('20'):
                                seed['pubTime'] = pubTime[0].strip()

                        if seed['pubTime'] > html_packed['end'].replace('-0', '-'):
                            continue
                        elif seed['pubTime'] < html_packed['start'].replace('-0', '-'):
                            break
                        seeds.append(seed)
                except Exception as e:
                    self.logger.error(str(e))
            else:
                if len(divs) > 0:
                    nextURL = tree.xpath('//div[@class="mod-page"]/div[@class="c-page"]/a[@title="下一页"]/@href'.decode('utf8'))
                    if len(nextURL) > 0:
                        seeds.append({
                            'url': 'http://news.p2peye.com' + nextURL[0] if nextURL[0].startswith('/') else nextURL[0],
                            'category': html_packed['category'],
                            'start': html_packed['start'],
                            'end': html_packed['end'],
                            'spider': 'Spider_bbsp2peye.crawl0',
                            'dont_filter': True,
                        })
        except Exception as e:
            self.logger.error(str(e))
        return [], seeds

    def parse1(self, html_packed):
        """ 文章(平台动态、网贷专栏、忘带新闻的帖子) """
        fields = []
        try:
            tree = etree.HTML(html_packed['html'].decode('gbk', 'ignore'))
            articleItem = ArticleItem()

            # 文章ID
            aid = re.findall('p2peye\.com/(thread-.*?)\.html', html_packed['url'])
            if len(aid) == 0:
                aid = re.findall('p2peye\.com/(article-.*?)\.html', html_packed['url'])
            if len(aid) > 0:
                articleItem.aid = aid[0]
                articleItem._id = 'p2peye-%s' % aid[0]

            # 文章链接
            articleItem.url = html_packed['url']

            # 文章标题
            title = tree.xpath('//div[@id="ct"]//h1[@id="plat-title"]/text()')
            if len(title) == 0:
                title = tree.xpath('//meta[@name="keywords"]/@content')
            if len(title) > 0:
                articleItem.title = title[0].strip()

            # 文章内容
            content = tree.xpath('//div[@id="ct"]//td[@id="article_content"]')
            if len(content) > 0:
                articleItem.content = etree.tounicode(content[0])

            # 文章描述
            description = tree.xpath('//meta[@name="description"]/@content')
            if len(description) > 0:
                articleItem.description = ' '.join(description).strip()
            elif 'description' in html_packed.keys():
                articleItem.description = html_packed['description']

            # 封面缩略图
            if 'coverImg' in html_packed.keys():
                articleItem.coverImg = html_packed['coverImg']

            txt = ' '.join(tree.xpath('//div[@id="ct"]//div[@class="c-a-inf"]//text()')).replace('\t', '').replace('\r', '').replace('\n', '').replace('  ', '')
            # 发布时间
            if 'pubTime' in html_packed.keys():
                try:
                    articleItem.pubTime = int(time.mktime(time.strptime(html_packed['pubTime'], '%Y-%m-%d %H:%M')))
                except Exception as e:
                    pass
            else:
                pubTime = re.findall('发布时间: ?(20.*?\d+:\d+)'.decode('utf8'), txt)
                if len(pubTime) > 0:
                    articleItem.pubTime = int(time.mktime(time.strptime(pubTime[0], '%Y-%m-%d %H:%M')))

            # 作者
            authorNickname = re .findall('原作者:(.*?) '.decode('utf8'), txt)
            if len(authorNickname) == 0:
                authorNickname = re .findall('发布者:(.*?)\|'.decode('utf8'), txt)
            if len(authorNickname) > 0:
                articleItem.authorNickname = authorNickname[0].split('|')[0].split('来自')[0].strip()

            # 点赞
            praiseCount = tree.xpath('//div[@id="ct"]//div[@id="click_div"]//a[@title="给力"]/span/text()'.decode('utf8'))
            if len(praiseCount) > 0:
                articleItem.praiseCount = int(praiseCount[0].strip())

            # 踩
            refuseCount = tree.xpath('//div[@id="ct"]//div[@id="click_div"]//a[@title="没劲"]/span/text()'.decode('utf8'))
            if len(refuseCount) > 0:
                articleItem.refuseCount = int(refuseCount[0].strip())

            # 阅读量
            readCount = re.findall('浏览量: ?(\d+)'.decode('utf8'), txt)
            if len(readCount) > 0:
                articleItem.readCount = int(readCount[0])
            elif 'readCount' in html_packed.keys():
                articleItem.readCount = html_packed['readCount']

            # 评论数
            if 'commentCount' in html_packed.keys():
                articleItem.commentCount = html_packed['commentCount']

            # 分类
            if 'category' in html_packed.keys():
                articleItem.classification = html_packed['category']

            # 文章来源
            source = re.findall('来自: ?(.*?)[ \|]'.decode('utf8'), txt)
            if len(source) > 0:
                articleItem.source = source[0]

            # 抓取来源
            articleItem.crawlSource = '网贷天眼'

            # 抓取时间
            articleItem.crawlTimestamp = html_packed['time_crawl']

            field = dict(articleItem.__dict__)
            field['pipeline_dbType'] = 'mongo'
            fields.append(field)

        except Exception as e:
            self.logger.error(str(e))
        return fields, []

    def parse2(self, html_packed):
        """ 曝光台 """
        seeds = []
        try:
            tree = etree.HTML(html_packed['html'].decode('gbk', 'ignore'))
            lis = tree.xpath('//ul[@role-parent="newloadmore"]/li')
            for li in lis:
                try:
                    seed = {
                        'spider': 'Spider_bbsp2peye.crawl0',
                        'start': html_packed['start'],
                        'end': html_packed['end'], 'category': html_packed['category'],
                        'pubTime': time.strftime('%Y-%m-%d %H:%M', time.localtime())
                    }

                    # URL
                    url = li.xpath('./a[@class="newlistbox"]/@href')
                    if len(url) > 0:
                        seed['url'] = 'http://www.p2peye.com' + url[0] if url[0].startswith('/thread') else url[0]

                        # 描述
                        description = ' '.join(li.xpath('./a/div[@class="synopsis"]/text()')).strip()
                        if len(description) > 0:
                            seed['description'] = description

                        # 发表时间
                        pubTime = li.xpath('./a/div/span[@class="time"]/text()')
                        if len(pubTime) > 0:
                            seed['pubTime'] = pubTime[0].strip()
                        if seed['pubTime'] > html_packed['end'].replace('-0', '-'):
                            continue
                        elif seed['pubTime'] < html_packed['start'].replace('-0', '-'):
                            break
                        seeds.append(seed)
                except Exception as e:
                    self.logger.error(str(e))
            else:
                if len(lis) > 0:
                    pageNum = re.findall('forum-\d+-(\d+)\.html', html_packed['url'])
                    if len(pageNum) > 0:
                        nextURL = html_packed['url'].replace('-%s.html' % pageNum[0], '-%s.html' % (int(pageNum[0]) + 1))
                        seeds.append({
                            'url': nextURL,
                            'category': html_packed['category'],
                            'start': html_packed['start'],
                            'end': html_packed['end'],
                            'spider': 'Spider_bbsp2peye.crawl0',
                            'dont_filter': True,
                        })
        except Exception as e:
            self.logger.error(str(e))
        return [], seeds

    def parse3(self, html_packed):
        """ 曝光帖子(曝光台帖子) """
        fields = []
        try:
            tree = etree.HTML(html_packed['html'].decode('gbk', 'ignore'))
            articleItem = ArticleItem()

            # 文章ID
            aid = re.findall('p2peye\.com/(thread-.*?)\.html', html_packed['url'])
            if len(aid) == 0:
                aid = re.findall('p2peye\.com/(article-.*?)\.html', html_packed['url'])
            if len(aid) > 0:
                articleItem.aid = aid[0]
                articleItem._id = 'p2peye-%s' % aid[0]

            # 文章URL
            articleItem.url = html_packed['url']

            # 文章标题
            title = tree.xpath('//meta[@name="keywords"]/@content')
            if len(title) > 0:
                articleItem.title = title[0]

            # 文章内容
            content = tree.xpath('//div[@class="typeoption"]/table[@summary]')
            if len(content) > 0:
                articleItem.content = etree.tounicode(content[0])

            # 文章描述
            description = tree.xpath('//meta[@name="description"]/@content')
            if len(description) > 0:
                articleItem.description = description[0]
            elif 'description' in html_packed.keys():
                articleItem.description = html_packed['description']

            # 发布时间
            pubTime = tree.xpath('//meta[@property="og:release_date"]/@content')
            if len(pubTime) > 0:
                try:
                    articleItem.pubTime = int(time.mktime(time.strptime(pubTime[0], '%Y-%m-%d %H:%M')))
                except Exception as e:
                    pass
            else:
                pubTime = ' '.join(tree.xpath('//div[@class="authi"]/em[contains(@id, "authorposton")]/text()'))
                pubTime = re.findall('20\d.*?\d*:\d*', pubTime)
                if len(pubTime) > 0:
                    try:
                        articleItem.pubTime = int(time.mktime(time.strptime(pubTime[0], '%Y-%m-%d %H:%M')))
                    except Exception as e:
                        pass

            # 作者昵称
            author = tree.xpath('//div[@class="pls favatar"]/div[@class="pi"]/div[@class="authi"]/a/text()')
            if len(author) == 0:
                author = tree.xpath('//div[@class="pls favatar"]//div/strong/a[@class="xi2"]/text()')
            if len(author) > 0:
                articleItem.authorNickname = author[0].strip()

            # 点赞数
            praise = tree.xpath('//a[@id="recommend_add"]/i/span[@id="recommendv_add"]/text()')
            if len(praise) > 0:
                try:
                    articleItem.praiseCount = int(praise[0])
                except Exception as e:
                    pass

            # 踩
            refuseCount = tree.xpath('//a[@id="recommend_subtract"]/i/span[@id="recommendv_subtract"]/text()')
            if len(refuseCount) > 0:
                try:
                    articleItem.refuseCount = int(refuseCount[0])
                except Exception as e:
                    pass

            spans = tree.xpath('//td/div[@class="hm ptn"]/span[@class="xi1"]')
            if len(spans) == 2:
                # 阅读数
                try:
                    articleItem.readCount = int(spans[0].xpath('./text()'))
                except Exception as e:
                    pass

                # 评论数
                try:
                    articleItem.commentCount = int(spans[1].xpath('./text()'))
                except Exception as e:
                    pass

            # 分享数
            shareCount = tree.xpath('//a[@class="sharep"]/i/span[@id="sharenumber"]')
            if len(shareCount) > 0:
                try:
                    articleItem.shareCount = int(shareCount[0])
                except Exception as e:
                    pass

            # 收藏数
            collectCount = tree.xpath('//a[@id="k_favorite"]/i/span[@id="favoritenumber"]/text()')
            if len(collectCount) > 0:
                try:
                    articleItem.collectCount = int(collectCount[0])
                except Exception as e:
                    pass

            # 分类
            if 'category' in html_packed.keys():
                articleItem.classification = html_packed['category']

            # 抓取来源
            articleItem.crawlSource = '网贷天眼'

            # 抓取时间
            articleItem.crawlTimestamp = html_packed['time_crawl'] if 'time_crawl' in html_packed.keys() else int(time.time())

            field = dict(articleItem.__dict__)
            field['pipeline_dbType'] = 'mongo'
            fields.append(field)
        except Exception as e:
            self.logger.error(str(e))
        return fields, []

    def parse4(self, html_packed):
        """ 平台官方动态 """
        seeds = []
        try:
            tree = etree.HTML(html_packed['html'])
            lis = tree.xpath('//div[@class="mod-list"]/ul/li[@class="item clearfix"]')
            for li in lis:
                try:
                    seed = {
                        'spider': 'Spider_bbsp2peye.crawl0',
                        'pubTime': time.strftime('%Y-%m-%d %H:%M', time.localtime())
                    }

                    # URL
                    url = li.xpath('./div[@class="mc-hd"]/a/@href')
                    if len(url) > 0:
                        seed['url'] = url[0]

                        # 描述
                        description = ' '.join(li.xpath('./div[@class="mc-bd"]/span/text()')).strip()
                        if len(description) > 0:
                            seed['description'] = description

                        commentCount = li.xpath('./div//span[@class="ft-comment"]/text()')
                        try:
                            seed['commentCount'] = int(commentCount[0])
                        except Exception as e:
                            pass

                        readCount = li.xpath('./div//span[@class="ft-see"]/text()')
                        try:
                            seed['readCount'] = int(readCount[0])
                        except Exception as e:
                            pass

                        # 发表时间
                        pubTime = li.xpath('./div/span[contains(@class, "time")]/text()')
                        if len(pubTime) > 0:
                            seed['pubTime'] = ':'.join(pubTime[0].strip().split(':')[:-1])      # 解析出来的是2018-01-09 14:29:00，只保留到分，即2018-01-09 14:29
                        if seed['pubTime'] > html_packed['end']:
                            continue
                        elif seed['pubTime'] < html_packed['start']:
                            break
                        seed['category'] = '官方动态'
                        seeds.append(seed)
                except Exception as e:
                    self.logger.error(str(e))
            else:
                if len(lis) > 0:
                    nextURL = tree.xpath('//div[contains(@class, "page")]/a[contains(text(), "下一页")]/@href'.decode('utf8'))
                    if len(nextURL) > 0:
                        nextURL = nextURL[0]
                        if nextURL.startswith('/gfdt'):
                            nextURL = html_packed['url'].split('/gfdt')[0] + nextURL
                        seeds.append({
                            'url': nextURL,
                            'start': html_packed['start'],
                            'end': html_packed['end'],
                            'spider': 'Spider_bbsp2peye.crawl0',
                            'dont_filter': True,
                        })
        except Exception as e:
            self.logger.error(str(e))
        return [], seeds



