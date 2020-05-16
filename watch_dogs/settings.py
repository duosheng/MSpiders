# encoding=utf-8

import host_settings


REDIS_HOST = 'localhost' if not hasattr(host_settings, 'REDIS_HOST') or len(host_settings.REDIS_HOST) == 0 else host_settings.REDIS_HOST
REDIS_PORT = 6379 if not hasattr(host_settings, 'REDIS_PORT') or host_settings.REDIS_PORT == 0 else host_settings.REDIS_PORT
REDIS_DB = 0
REDIS_PASSWORD = None if not hasattr(host_settings, 'REDIS_PASS') or len(host_settings.REDIS_PASS) == 0 else host_settings.REDIS_PASS
REDIS_KEYNAME = 'Seeds'

MONGO_HOST = 'localhost' if not hasattr(host_settings, 'MONGO_HOST') or len(host_settings.MONGO_HOST) == 0 else host_settings.MONGO_HOST
MONGO_PORT = 27017 if not hasattr(host_settings, 'MONGO_PORT') or host_settings.MONGO_PORT == 0 else host_settings.MONGO_PORT
MONGO_USER = '' if not hasattr(host_settings, 'MONGO_USER') or len(host_settings.MONGO_USER) == 0 else host_settings.MONGO_USER
MONGO_PASS = '' if not hasattr(host_settings, 'MONGO_PASS') or len(host_settings.MONGO_PASS) == 0 else host_settings.MONGO_PASS


Downloader_LOGPATH = "/data/logs/" if not hasattr(host_settings, 'Downloader_LOGPATH') or host_settings.Downloader_LOGPATH == 0 else host_settings.Downloader_LOGPATH
Analyzer_LOGPATH = "/data/logs/" if not hasattr(host_settings, 'Analyzer_LOGPATH') or host_settings.Analyzer_LOGPATH == 0 else host_settings.Analyzer_LOGPATH
WatchDog_LOGPATH = "/data/logs/" if not hasattr(host_settings, 'WatchDog_LOGPATH') or host_settings.WatchDog_LOGPATH == 0 else host_settings.WatchDog_LOGPATH
DingDingNoticeUrl = 'https://oapi.dingtalk.com/robot/send?access_token=2752ad4d8c3ff44ec1bc5e5b4ea3a1243ce49ef229fbf083bb30d391f07de0f9' if not hasattr(host_settings, 'DingDingNoticeUrl') or len(host_settings.DingDingNoticeUrl) == 0 else host_settings.DingDingNoticeUrl

# 执行计划
PLANS = [
    # {'name': 'job_bbswdzj', 'hour': 3, 'isProxy': False, 'spider': 'bbswdzj'},  # 网贷之家社区
    # {'name': 'job_bbsp2peye0', 'hour': 3, 'isProxy': False, 'spider': 'bbsp2peye'},  # 网贷天眼社区
    # {'name': 'job_bbsp2peye1', 'hour': 3, 'isProxy': False, 'spider': 'bbsp2peye'},  # 网贷天眼平台官方动态


    {'name': 'job_gdeegd', 'hour': 2, 'isProxy': False, 'spider': 'gdeegd'},  # gdstc爬虫定时任务，每天凌晨3点执行一次
    {'name': 'job_comgdgov', 'hour': 2, 'isProxy': False, 'spider': 'comgdgov'},  # gdstc爬虫定时任务，每天凌晨3点执行一次
    {'name': 'job_gdstc', 'hour': 3, 'isProxy': False, 'spider': 'gdstc'},  # gdstc爬虫定时任务，每天凌晨3点执行一次
    {'name': 'job_amrgd', 'hour': 3, 'isProxy': False, 'spider': 'amrgd'},  # gdstc爬虫定时任务，每天凌晨3点执行一次
    {'name': 'job_nrgd', 'hour': 3, 'isProxy': False, 'spider': 'nrgd'},  # gdstc爬虫定时任务，每天凌晨3点执行一次


]
