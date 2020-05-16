# coding=utf-8

import time
import uuid


class ArticleItem(object):
    def __init__(self):
        self._id = str(uuid.uuid1())  # 文章ID uuid.uuid1()
        self.aid = ''  # 文章原来的ID
        self.url = ''  # 文章的url
        self.title = ''  # 文章标题
        self.content = ''  # 文章内容
        self.description = ''  # 文章描述
        self.tags = ''  # 标签
        self.coverImg = ''  # 缩略图
        self.pubTime = int(time.time())  # 发布时间(存时间戳)timestamp
        self.authorNickname = ''  # 作者昵称
        self.authorID = ''  # 作者ID
        self.praiseCount = 0  # 点赞数
        self.refuseCount = 0  # 踩
        self.readCount = 0  # 阅读数
        self.commentCount = 0  # 评论数
        self.shareCount = 0  # 转载/分享数
        self.collectCount = 0  # 收藏数
        self.rewardCount = 0  # 打赏
        self.classification = ''  # 分类
        self.source = ''  # 文章来源
        self.crawlSource = ''  # 爬取来源
        self.crawlTimestamp = int(time.time())  # 抓取时间(存时间戳)timestamp


class TopicItem(object):
    def __init__(self):
        self._id = str(uuid.uuid1())  # 网站名-话题ID
        self.tid = ''   # 话题ID
        self.classification = ''    # 所属分类
        self.url = ''  # 话题url
        self.title = ''  # 话题标题
        self.content = ''  # 话题内容
        self.postings = 0   # 帖子数量
        self.member = 0     # 参与讨论的人数


class CommentItem(object):
    def __init__(self):
        self._id = ''  # 评论id uuid.uuid1()
        self.articleId = ''  # 文章id
        self.reviewerId = ''  # 评论人ID
        self.reviewerName = ''  # 评论人名称
        self.comment = ''  # 评论内容
        self.reviewerTimestamp = int(time.time())  # 评论时间
        self.quoteId = ''  # 引用的评论ID


class StocksArticleItem(object):
    def __init__(self):
        self._id = ''  # 股票文章id uuid.uuid1()
        self.code = ''  # 股票代码
        self.crawlTimeStamp = int(time.time())  # 抓取时间(存时间戳)timestamp
        self.pubTime = ''  # 股票文章的发布时间(存时间戳)
        self.classification = ''  # 分类
        self.crawlSource = ''  # 爬取来源
        self.url = ''  # 股票文章的url
        self.title = ''  # 股票文章的标题


class ResearchReport(object):
    def __init__(self):
        self._id = ''  # 研报数据id
        self.code = ''  # 股票代码
        self.crawlTimeStamp = int(time.time())  # 抓取时间(存时间戳)timestamp
        self.pubTime = ''  # 研报数据日期（存时间戳）
        self.crawlSource = ''  # 爬取来源
        self.url = ''  # 研报数据的url
        self.title = ''  # 研报数据的标题
        self.author = ''  # 研报数据的作者
        self.change = ''  # 评级变动
        self.insName = ''  # 评级机构名称
        self.sratingName = ''  # 评级
        self.content = ''  # 研报文章内容

        # 新增个股评级汇总的数据(半年内)
        self.ratingNumofbuy = 0       # 评级买入家数
        self.ratingNumofoutperform = 0    # 评级增持家数
        self.ratingNumofhold = 0       # 评级中性家数
        self.ratingNumofunderperform = 0    # 评级减持家数
        self.ratingNumofsell = 0        # 评级卖出家数

class StockQuote(object):
    def __init__(self):
        self._id = ''  # 报价数据id
        self.updatetime = int(time.time())  # 抓取时间(存时间戳)timestamp
        # self.stockTypeID = ''  # 股票类型
        self.code = ''  # 股票代码
        self.name = ''  # 股票名称
        self.last = 0.0  # 最新价
        self.buy = 0.0    # 买入
        self.sell = 0.0   # 卖出
        self.preclose = 0.0  # 昨收
        self.open = 0.0  # 今开
        self.high = 0.0  # 最高
        self.low = 0.0  # 最低
        self.vol = 0.0  # 成交量
        self.amount = 0.0  # 成交额
        self.day = ''   # 年月日
        self.hour = ''  # 时分秒
        self.time = 0   # 当前行情时间(存时间戳)


class StockExemption(object):
    def __init__(self):
        self._id = ''   #报价数据id
        self.crawlTimeStamp = int(time.time())  # 抓取时间(存时间戳)timestamp
        self.bonusimpdate = ''  # 分红公告日期
        self.bonusyear = ''     # 分红实施年度
        self.cur = ''           # 派现币种
        self.bonusskratio = 0.0  # 送股比例（10送X）
        self.tranaddskraio = 0.0    # 转增股比例（10转增X）
        self.recorddate = ''    # 股权登记日
        self.exrightdate = ''   # 除权除息日
        self.cdividend = 0.0     # 税前红利（元）
        self.fdividendbh = 0.0   # 税前红利（美元）
        self.tranaddsklistdate = ''  # 转增股上市日
        self.bonussklistdate = ''   # 送股上市日
        self.tranaddskaccday = ''   # 转增股到帐日
        self.bonusskaccday = ''     # 送股到账日

        self.symbol = ''
        self.secode = ''
        self.divitype = ''      # 除权类型
        self.taxfdividendbh = 0.0
        self.taxcdividend = 0.0
        self.divibegdate = ''
        self.summarize = ''

        self.url = ''
        self.code = ''
