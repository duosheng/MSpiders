# encoding=utf-8
# ---------------------------------------
#   版本：0.1
#   日期：2016-04-26
#   作者：code pande
#   开发环境：Win64 + Python 2.7
# ---------------------------------------

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from MSpiders_Downloader.Downloader import beginer


if __name__ == '__main__':
    beginer.begin()
