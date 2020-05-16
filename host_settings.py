# encoding=utf-8
# 功能：将几个数据库的host放到这里，只要在此处填入数据库地址即可，以后更新代码可以直接将其他文件覆盖。
import datetime
import os
# 生产redis
# REDIS_HOST = os.environ.get("REDIS_HOST", '106.75.130.134')
# REDIS_PORT = int(os.environ.get("REDIS_PORT", 26379))
# REDIS_PASS = os.environ.get("REDIS_PASS", 'catspider')

# 测试环境redis
REDIS_HOST = os.environ.get("REDIS_HOST", '127.0.0.1')
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
# REDIS_PASS = os.environ.get("REDIS_PASS", 'bigdatalyra')

# 本地环境redis
# REDIS_HOST = os.environ.get("REDIS_HOST", 'localhost')
# REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
# REDIS_PASS = os.environ.get("REDIS_PASS", '')

# 生产环境mongodb
# MONGO_HOST = os.environ.get("MONGO_HOST", '106.75.130.134')
# MONGO_PORT = int(os.environ.get("MONGO_PORT", 27017))
# MONGO_USER = os.environ.get("MONGO_USER", 'cat_spider_api')
# MONGO_PASS = os.environ.get("MONGO_PASS", 'cat_spider_api')

# 测试环境mongodb
MONGO_HOST = os.environ.get("MONGO_HOST", '192.168.104.147')
MONGO_PORT = int(os.environ.get("MONGO_PORT", 27017))
MONGO_USER = os.environ.get("MONGO_USER", '')
MONGO_PASS = os.environ.get("MONGO_PASS", '')



ES_HOST = os.environ.get("ES_HOST", '')
DingDingNoticeUrl = os.environ.get("DingDingNoticeUrl", '')

# 日志配置
# Downloader_LOGPATH = 'D:\git_python_project\MSpiders\MSpiders_Downloader\\'
# Analyzer_LOGPATH = 'D:\git_python_project\MSpiders\MSpiders_Analyzer\\'

Downloader_LOGPATH = 'D:\\logs\\MSpider\\downloader\\'
Analyzer_LOGPATH = 'D:\\logs\\MSpider\\analyzer\\'
WatchDog_LOGPATH = 'D:\\logs\\MSpider\\watchdogs\\'

LOG_SAVE = True
LOG_LEVEL = 'DEBUG'     # DEBUG/INFO/WARNING/ERROR


