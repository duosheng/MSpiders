# encoding=utf-8
import base64
import json
import logging


import requests
from xml.dom.minidom import parseString

from urllib3 import encode_multipart_formdata

logger = logging.getLogger('root')

cookie = "JSESSIONID=FD9B432DBF5E48D1C7AF582EE35929D7; resolution=1920; i18next=zh-CN; loginStatus=0; skinname=default; JSESSIONID=A4F9DE569C8DC11AB25924C7045B4AFB; PAGEID=2128fabd-f3c0-412d-b808-3ece7dc7c026; CURRENT_USER_DIGITALID=\"eHVsaQ==\""

headers = {
            'Cookie': cookie,
            'Accept-Encoding': "gzip, deflate",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36",
            'If-Modified-Since': "Thu, 16 Apr 2020 08:11:20 GMT",
            'Accept': "*/*",
            'Referer': "http://test.gzjirui.com/magicflu/html/form/records2.jsp?spaceId=93d0b958-52d3-4858-b6e9-344a23aede67&formId=-1",
            'X-Requested-With': "XMLHttpRequest",
            'Connection': "keep-alive",
            'X-FirePHP-Version': "0.0.6",
            'Cache-Control': "no-cache",
            'Postman-Token': "00188fd1-15c6-73d1-aa0f-577970b6d59d"
        }

class FFWBAPI(object):

    def __init__(self, space_id, table_id):
        self.space_id = space_id
        self.table_id = table_id

    def upload_file(self, id, file_path):
        url = "http://test.gzjirui.com/magicflu/service/s/%s/forms/%s/records/%s/txt/attachments?jqUpload" % (self.space_id, self.table_id, id)
        filename = file_path.split('\\')[-1]
        file_data = {
            "files": (filename, open(file_path, 'rb').read())
        }
        encode_data = encode_multipart_formdata(file_data)
        data = encode_data[0]

        headers = {
            'content-type': encode_data[1],
            'Cookie': cookie,
            'Origin': "http://test.gzjirui.com",
            'Accept-Encoding': "gzip, deflate",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36",
            'Accept': "application/json, text/javascript, */*; q=0.01",
            'Referer': "http://test.gzjirui.com/magicflu/html/upload/upload.jsp?single=true&upload_url=%2Fmagicflu%2Fservice%2Fs%2F93d0b958-52d3-4858-b6e9-344a23aede67%2Fforms%2F2717074e-7886-4495-9a0e-4733e55098d2%2Frecords%2F12%2Ftxt%2Fattachments%3FjqUpload&file_size_limit=8000000&file_types=*.*&file_types_description=%E6%89%80%E6%9C%89%E6%96%87%E4%BB%B6",
            'X-Requested-With': "XMLHttpRequest",
            'Connection': "keep-alive",
            'X-FirePHP-Version': "0.0.6",
            'Cache-Control': "no-cache",
            'Postman-Token': "e7a8f7b7-3889-5ece-5642-a57b2b01df10"
        }
        response = requests.post(url, headers=headers, data=data)
        print(response.text)


    def insert_record(self, data):
        url = "http://test.gzjirui.com/magicflu/service/s/jsonv2/%s/forms/%s/records" % (self.space_id, self.table_id)
        payload = {
            "zhuguanbumen1": data['spider'],
            "wangzhanleixing": data['type'],
            "fid": data['fid'],
            "contentlink": data['url'],
            "title": data['title'],
            "createtime": data['pushTime'],  # 2020-03-10
            # "content": data['content'][0:2000],
            # "page": data['page'],
            "shenbaoshijian": data['pushTime'],
            "wangye": data['page'],
            "zhengwenzishu": data['len']  # "300"
        }
        content = data['content']
        c = 3000
        for i in range(len(content) // c + 1):
            start = i * c
            end = (i+1)*c
            if(i == 0):
                payload['content'] = content[start:end]
            else:
                payload['content' + str(i)] = content[start:end]

        # page = data['page']
        # for i in range(len(page) // c):
        #     start = i * c
        #     end = (i + 1) * c
        #     payload['page' + str(i)] = page[start:end]

        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
        if(response.status_code==200 or response.status_code==201):
            errcode = json.loads(response.text)['errcode']
        print(response.text)


    def get_id(self, fid):
        """
        根据fid 转换成id
        """
        url = "http://test.gzjirui.com/magicflu/service/s/%s/forms/%s/records/feed" % (self.space_id, self.table_id)
        querystring = {
            "currentUserId": "",
            "start": "0",
            "limit": "16",
            "bq": "fid(eq):_%s&&id(orderby):asc" % bytes.decode(base64.b64encode(str(fid).encode("utf-8"))),
            "pureExternalQuery": "",
        }
        id = None
        try:
            response = requests.request("GET", url, headers=headers, params=querystring)
            doc = parseString(response.text)
            id = doc.getElementsByTagName('id')[0].childNodes[0].data
        except Exception as e:
            logger.error("保存到魔方网表失败： error： %s" % str(e))
        return id

    def download_accessory(self, files):
        file_paths = []
        for file in files:
            # 下载附件
            down_res = requests.get(url=file['file_url'], headers=headers)
            file_path = 'D:\\data\\files\\%s.%s' % (file['file_name'], file['file_type'])
            with open(file_path, "wb") as code:
                code.write(down_res.content)
            file_paths.append(file_path)
        return file_paths





if __name__ == '__main__':
    space_id = "93d0b958-52d3-4858-b6e9-344a23aede67"
    table_id = "2717074e-7886-4495-9a0e-4733e55098d2"
    ffwbapi = FFWBAPI(space_id=space_id, table_id=table_id)
    # insert_record()
    # upload_file()
    id = ffwbapi.get_id(8)
    print(id)
