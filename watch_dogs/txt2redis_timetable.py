# encoding=utf-8

import os
import re
import glob
import redis

from watch_dogs import settings

if __name__ == '__main__':
    rconn = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB, password=settings.REDIS_PASSWORD)
    filenames = glob.glob('timetable*')
    for filename in filenames:
        spider = re.findall('timetables_(.*?)\.txt', filename)
        if len(spider) > 0:
            spider = spider[0]
            with open(filename, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if len(line.strip()) > 0:
                        rconn.lpush('Timetable:%s' % spider, line.strip())
        os.remove(filename)
    print('Finish!')












