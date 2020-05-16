# coding=utf-8
import requests
from urllib3 import encode_multipart_formdata

url = "http://test.gzjirui.com/magicflu/service/s/93d0b958-52d3-4858-b6e9-344a23aede67/forms/2717074e-7886-4495-9a0e-4733e55098d2/records/12/txt/attachments?jqUpload"

querystring = {"jqUpload":""}

filepath = "/data/file/关于开展“广东省中小学生研学实践教育基（营）地”推荐工作的通知.pdf"
filename = "关于开展“广东省中小学生研学实践教育基（营）地”推荐工作的通知.pdf"
# 第二种方法：
file_data = {
    "files" : (filename, open(filepath,'rb').read())
}
encode_data = encode_multipart_formdata(file_data)
data = encode_data[0]


headers = {
    'content-type': encode_data[1],
    'Cookie': "JSESSIONID=39C1E18D8BE3BD69BE9E2D50B2EBE6A1; JSESSIONID=70BA542B7E9A7254702EAF30C2A7858D; PAGEID=ec78509b-66f7-47c0-97d6-394176f27e73; resolution=1920; loginStatus=0; skinname=default; i18next=zh-CN; CURRENT_USER_DIGITALID=\"eHVsaQ==\"",
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

res = requests.post(url, headers=headers, data=data).json()
print(res)





