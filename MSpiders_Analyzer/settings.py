# encoding=utf-8

import host_settings

REDIS_HOST = 'localhost' if not hasattr(host_settings, 'REDIS_HOST') or len(host_settings.REDIS_HOST) == 0 else host_settings.REDIS_HOST
REDIS_PORT = 6379 if not hasattr(host_settings, 'REDIS_PORT') or host_settings.REDIS_PORT == 0 else host_settings.REDIS_PORT
REDIS_PASS = '' if not hasattr(host_settings, 'REDIS_PASS') or len(host_settings.REDIS_PASS) == 0 else host_settings.REDIS_PASS
MONGO_HOST = '192.168.104.147' if not hasattr(host_settings, 'MONGO_HOST') or len(host_settings.MONGO_HOST) == 0 else host_settings.MONGO_HOST
MONGO_PORT = 27017 if not hasattr(host_settings, 'MONGO_PORT') or host_settings.MONGO_PORT == 0 else host_settings.MONGO_PORT
MONGO_USER = '' if not hasattr(host_settings, 'MONGO_USER') or len(host_settings.MONGO_USER) == 0 else host_settings.MONGO_USER
MONGO_PASS = '' if not hasattr(host_settings, 'MONGO_PASS') or len(host_settings.MONGO_PASS) == 0 else host_settings.MONGO_PASS
ES_HOST = '192.168.104.147' if not hasattr(host_settings, 'ES_HOST') or len(host_settings.ES_HOST) == 0 else host_settings.ES_HOST


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

# 去重队列
Filter_host = REDIS_HOST
Filter_port = REDIS_PORT
Filter_db = 0
Filter_keyName = 'bloomfilter'
Filter_password = REDIS_PASS

Num_process = 1  # 进程数
Num_gevent = 2  # 每条进程里面的协程数
Timeout_gevent = 60  # 协程的超时时间，单位秒

Log_level = 'INFO'  # DEBUG/INFO/WARNING/ERROR
Log_save = True  # 是否将日志保存到本地

SPECIAL_TAG = ';;;;'  # 文本分割占位符

ERRORMAX_items = 10  # 某个爬虫连续失败超过ERRORMAX次报警
ERRORMAX_seeds = 5

MSG_Whitelist = ['WeChat', ]

DingDingNoticeUrl = 'https://oapi.dingtalk.com/robot/send?access_token=2752ad4d8c3ff44ec1bc5e5b4ea3a1243ce49ef229fbf083bb30d391f07de0f9' if not hasattr(host_settings, 'DingDingNoticeUrl') or len(host_settings.DingDingNoticeUrl) == 0 else host_settings.DingDingNoticeUrl

Parser_bbsp2peye = {
    'mongo': {
        'host': MONGO_HOST,
        'port': MONGO_PORT,
        'db': 'community',
        'collection': 'articles',
        'account': MONGO_USER,
        'password': MONGO_PASS,
    },
    'es': {
        'host': ES_HOST,
        'port': 9200,
        'index': 'community',
        'doc_type': 'articles',
    },
}

Parser_gdstc = {
    'ffwb': {
        'host': '93d0b958-52d3-4858-b6e9-344a23aede67',
        'port': '2717074e-7886-4495-9a0e-4733e55098d2'
    }
}


Parser_amrgd = {
    'ffwb': {
        'host': '93d0b958-52d3-4858-b6e9-344a23aede67',
        'port': '2717074e-7886-4495-9a0e-4733e55098d2'
    }
}

Parser_nrgd = {
    'ffwb': {
        'host': '93d0b958-52d3-4858-b6e9-344a23aede67',
        'port': '2717074e-7886-4495-9a0e-4733e55098d2'
    }
}

Parser_gdeegd = {
    'ffwb': {
        'host': '93d0b958-52d3-4858-b6e9-344a23aede67',
        'port': '2717074e-7886-4495-9a0e-4733e55098d2'
    }
}

Parser_comgdgov = {
    'ffwb': {
        'host': '93d0b958-52d3-4858-b6e9-344a23aede67',
        'port': '2717074e-7886-4495-9a0e-4733e55098d2'
    }
}
