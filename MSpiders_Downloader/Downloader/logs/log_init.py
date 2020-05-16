# encoding=utf-8


import logging
import host_settings as settings
from common.handlers import SafeRotatingFileHandler


def log_setlevel(level=None, ch=None, fh=None):
    if ch:
        ch.setLevel(level)
    if fh:
        fh.setLevel(level)


# 设置log格式，无法封装。。
logger = logging.getLogger('root')
fh = SafeRotatingFileHandler(filename='%s/downloader.log' % settings.Downloader_LOGPATH, when='D', interval=1, backupCount=7) if settings.LOG_SAVE else None
ch = logging.StreamHandler()
if settings.LOG_LEVEL.upper() == 'DEBUG':
    log_setlevel(logging.DEBUG, ch, fh)
elif settings.LOG_LEVEL.upper() == 'INFO':
    log_setlevel(logging.INFO, ch, fh)
elif settings.LOG_LEVEL.upper() == 'WARNING':
    log_setlevel(logging.WARNING, ch, fh)
elif settings.LOG_LEVEL.upper() == 'ERROR':
    log_setlevel(logging.ERROR, ch, fh)
formatter = logging.Formatter('%(asctime)s [%(levelname)s]: (%(filename)s-%(funcName)s-%(lineno)s) %(message)s', '%Y-%m-%d %H:%M:%S')
# formatter = logging.Formatter('%(created)f [%(levelname)s]: %(message)s', "%Y%b%d-%H:%M:%S")
if fh:
    fh.setFormatter(formatter)
    logger.addHandler(fh)
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(ch.level)
