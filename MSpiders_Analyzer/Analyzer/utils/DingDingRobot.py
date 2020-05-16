# coding=utf-8

import json
import requests
from MSpiders_Downloader.settings import DingDingNoticeUrl, MSG_Whitelist


def sendMsg(txt):
    try:
        for one in MSG_Whitelist:
            if isinstance(one, list):
                for elem in one:
                    if elem.lower() not in txt.lower():
                        break
                else:
                    return
            elif isinstance(one, str):
                if one.lower() in txt.lower():
                    return
        data = {"msgtype": "text", "text": {"content": txt}, "at": {"isAtAll": False}}
        requests.post(DingDingNoticeUrl, data=json.dumps(data), headers={"Content-type": "application/json"})
    except Exception as e:
        pass
