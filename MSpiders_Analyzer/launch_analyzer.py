# encoding=utf-8

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from MSpiders_Analyzer.Analyzer import beginer


if __name__ == '__main__':
    beginer.begin()
