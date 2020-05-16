# encoding=utf-8
# ---------------------------------------
#   语言：Python2.7
#   日期：
#   作者：
#   功能：爬虫监控调度
# ---------------------------------------
import datetime
import os
import sys
import time
import traceback

import requests

from watch_dogs import settings, jobs
from watch_dogs.utils import writeLog, RCONN, sendMsg

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from multiprocessing.dummy import Process


def isContinue(e1, e2):
    if isinstance(e1, tuple):
        if len(e1) == 2 and not e1[0] <= e2 <= e1[1]:
            return 1
    elif isinstance(e1, list):
        if e2 not in e1:
            return 1
    elif isinstance(e1, int):
        if e1 != e2:
            return 1


def tasks_dog():
    """
        任务调度时间主要有七种：weekday、day、daystep、hour、hourstep、minute、minutestep。
        weekday、day、hour、minute三种类型：整型、list、tuple。(hour=3表示每天3点执行，hour=[3,4,5]表示每天3,4,5点都执行一次，hour=(3,6)表示每天3~6点每个小时都执行一次）。
        daystep、hourstep、minutestep为整型。（hourstep=3表示每个3个小时执行一次）。
    """
    start = datetime.datetime.now()
    while True:
        now = datetime.datetime.now()
        weekday = now.weekday() + 1
        day = now.day
        hour = now.hour
        minute = now.minute
        tasks = []
        for plan in settings.PLANS:
            if 'times' not in plan.keys():
                plan['times'] = 0

            if 'weekday' in plan.keys():  # 以下判断时间是否不符合，不符合要求时continue跳过。
                if isContinue(plan['weekday'], weekday) == 1:
                    continue
            if 'day' in plan.keys():
                if isContinue(plan['day'], day) == 1:
                    continue
            if 'daystep' in plan.keys():
                if isinstance(plan['daystep'], int):
                    if plan['daystep'] == 0 or (now - start).days % plan['daystep'] != 0:
                        continue

            if (
                    'weekday' in plan.keys() or 'day' in plan.keys() or 'daystep' in plan.keys()) and 'hour' not in plan.keys() and 'hourstep' not in plan.keys():
                plan['hour'] = start.hour
            if 'hour' in plan.keys():
                if isContinue(plan['hour'], hour) == 1:
                    continue
            if 'hourstep' in plan.keys():
                if isinstance(plan['hourstep'], int):
                    difference = (now - start).seconds / 3600
                    if plan['hourstep'] == 0 or difference % plan['hourstep'] != 0 or difference / plan['hourstep'] != \
                            plan['times']:
                        continue

            if (
                    'hour' in plan.keys() or 'hourstep' in plan.keys()) and 'minute' not in plan.keys() and 'minutestep' not in plan.keys():
                plan['minute'] = start.minute
            if 'minute' in plan.keys():
                if isContinue(plan['minute'], minute) == 1:
                    continue
            if 'minutestep' in plan.keys():
                if isinstance(plan['minutestep'], int):
                    difference = int((now - start).total_seconds()) / 60  # 过去了多少分钟
                    if difference / plan['minutestep'] > plan['times']:
                        plan['times'] = difference / plan['minutestep']
                    if plan['minutestep'] == 0 or difference % plan['minutestep'] != 0 or difference / plan[
                        'minutestep'] != plan['times']:
                        continue
            plan['times'] += 1
            tasks.append(getattr(jobs, plan['name']))

        writeLog("Total task to run : {}".format(len(tasks)))
        for task in tasks:
            try:
                task()
            except Exception as e:
                """执行任务异常"""
                msg = traceback.format_exc()  # 方式1
                writeLog("run task exception: %s" % msg)

        sleep_time = 60 - datetime.datetime.now().second
        writeLog('tasks_dog sleeping...{}'.format(sleep_time))
        time.sleep(sleep_time)

def proxies_dog():
    while True:
        for plan in settings.PLANS:
            if 'isProxy' in plan.keys() and plan['isProxy'] is True:
                if RCONN.llen('Proxies:%s' % plan['spider']) <= 3:
                    writeLog('Proxies:%s need IP ... ' % plan['spider'])
                    try:
                        RCONN.delete('Proxies:%s' % plan['spider'])
                    except Exception as e:
                        pass
                    failure = 0
                    num = 0
                    while failure < 3:
                        try:
                            r = requests.get(
                                'http://dps.kuaidaili.com/api/getdps/?orderid=969999783818434&num=200&sep=2',
                                timeout=10)
                            if r.status_code == 200:
                                txts = r.content.split('\n')
                                for txt in txts:
                                    js = {'http': 'http://%s' % txt, 'https': 'http://%s' % txt}
                                    RCONN.lpush('Proxies:%s' % plan['spider'], str(js))
                                    num += 1
                            break
                        except Exception as e:
                            failure += 1
                    writeLog('Successful Proxies:%s (%s)' % (plan['spider'], num))
        writeLog('proxies_dog sleeping...')
        time.sleep(60)


def failure_dog():
    while True:
        failureNames = RCONN.keys('Failure:*')
        for one in failureNames:
            length = RCONN.llen(one)
            length_drop = 0
            for i in range(length):
                txt = RCONN.rpop(one)
                js = eval(txt)
                if 'failureCount' in js.keys() and js['failureCount'] < 4:
                    RCONN.lpush(settings.REDIS_KEYNAME, txt)
                else:
                    length_drop += 1
            writeLog('Roll Failure_%s back to Seeds: %s (drop %s)' % (length, one, length_drop))
            sendMsg('Roll Failure_%s back to Seeds: %s (drop %s)' % (length, one, length_drop))
        time.sleep(3600)


if __name__ == '__main__':
    tasks = [
        Process(target=tasks_dog),
        Process(target=proxies_dog),
        Process(target=failure_dog),
    ]
    for task in tasks:
        task.start()
    for task in tasks:
        task.join()
