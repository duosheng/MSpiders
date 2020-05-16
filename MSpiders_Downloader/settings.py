# encoding=utf-8
# ---------------------------------------
#   版本：0.1
#   日期：2016-04-26
#   作者：九茶<bone_ace@163.com>
#   开发环境：Win64 + Python 2.7
# ---------------------------------------

import host_settings

REDIS_HOST = 'localhost' if not hasattr(host_settings, 'REDIS_HOST') or len(host_settings.REDIS_HOST) == 0 else host_settings.REDIS_HOST
REDIS_PORT = 6379 if not hasattr(host_settings, 'REDIS_PORT') or host_settings.REDIS_PORT == 0 else host_settings.REDIS_PORT
REDIS_PASS = '' if not hasattr(host_settings, 'REDIS_PASS') or len(host_settings.REDIS_PASS) == 0 else host_settings.REDIS_PASS


# 消息队列中的SEED队列
Queue_seed_type = 'Queue_Redis'
Queue_seed_host = REDIS_HOST
Queue_seed_port = REDIS_PORT
Queue_seed_keyName = 'Seeds'
Queue_seed_password = REDIS_PASS

# 消息队列中的HTML队列
Queue_html_type = 'Queue_Redis'
Queue_html_host = REDIS_HOST
Queue_html_port = REDIS_PORT
Queue_html_keyName = 'Htmls'
Queue_html_password = REDIS_PASS

Num_process = 1  # 进程数
Num_gevent = 1  # 每条进程里面的协程数
Timeout_gevent = 60  # 协程的超时时间，单位秒

Log_level = 'INFO'  # DEBUG/INFO/WARNING/ERROR
Log_save = True  # 是否将日志保存到本地

ERRORMAX = 3  # 某个爬虫连续失败超过ERRORMAX次报警

DingDingNoticeUrl = 'https://oapi.dingtalk.com/robot/send?access_token=2752ad4d8c3ff44ec1bc5e5b4ea3a1243ce49ef229fbf083bb30d391f07de0f9' if not hasattr(host_settings, 'DingDingNoticeUrl') or len(host_settings.DingDingNoticeUrl) == 0 else host_settings.DingDingNoticeUrl

MSG_Whitelist = ['WeChat', ]

Spider_bbsp2peye = {
    'DELAY': 0.5,
    'RETRY': 2,
    'ISPROXY': False,
}

Spider_gdstc = {
    'DELAY': 1,
    'RETRY': 2,
    'ISPROXY': False,
}

Spider_scjgjjs = {
    'DELAY': 1,
    'RETRY': 2,
    'ISPROXY': False,
}

Spider_amrgd = {
    'DELAY': 1,
    'RETRY': 2,
    'ISPROXY': False,
}

Spider_nrgd = {
    'DELAY': 1,
    'RETRY': 2,
    'ISPROXY': False,
}

Spider_gdeegd = {
    'DELAY': 1,
    'RETRY': 2,
    'ISPROXY': False,
}

Spider_comgdgov = {
    'DELAY': 1,
    'RETRY': 2,
    'ISPROXY': False,
}
