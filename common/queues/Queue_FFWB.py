# encoding=utf-8
# ---------------------------------------
#   功能：数据对接数字魔方
# ---------------------------------------


import pymongo

from common import QueueBase
from common.queues.ffwb import FFWBAPI


class Queue_FFWB(QueueBase.QueueBase):
    def __init__(self, host='localhost', port=27017, **kwargs):
        # QueueBase.QueueBase.__init__(self, host, port)
        # space_id = "93d0b958-52d3-4858-b6e9-344a23aede67"
        # table_id = "2717074e-7886-4495-9a0e-4733e55098d2"
        self.ffwbapi = FFWBAPI(space_id=host, table_id=port)

    @QueueBase.catch
    def put(self, value, *args, **kwargs):
        self.ffwbapi.insert_record(data=value)
        id = self.ffwbapi.get_id(fid=value['fid'])
        # 下载附件
        file_paths = self.ffwbapi.download_accessory(value['files'])
        # 上传附件
        for f in file_paths:
            self.ffwbapi.upload_file(id=id, file_path=f)

    @QueueBase.catch
    def get(self, *args, **kwargs):
        pass

    @QueueBase.catch
    def update(self, value, *args, **kwargs):
        pass

    @QueueBase.catch
    def size(self, *args, **kwargs):
        pass
