# -*- coding: utf-8 -*-
# 2017/2/11 0011
# JEFF
import time
import pymongo
from news163_2 import settings


class TimeTool(object):
    @staticmethod
    def current_time(spec_full=None, spec_simple=None):
        return TimeTool.format_time(spec_full=spec_full, spec_simple=spec_simple)

    @staticmethod
    def format_time(timex=None, format_spec='%Y-%m-%d %H:%M:%S', spec_full=None, spec_simple=None):
        if spec_full:
            return time.strftime('%Y-%m-%d %H:%M:%S')
        if spec_simple:
            return time.strftime('%Y-%m-%d')
        return time.strftime(format_spec, time.localtime(timex))


class DbTool(object):
    client = pymongo.MongoClient()
    DB = client[settings.MONGODBNAME]

    @staticmethod
    def get_mongocoll_by_channel(channel=None):
        if not channel:
            return DbTool.DB['other_coll']
        if channel not in settings.CHANNEL_LIST:
            return DbTool.DB['other_coll']
        return DbTool.DB[settings.COLLECTNAME.format(channel)]


if __name__ == '__main__':
    print(TimeTool.current_time())
    print(TimeTool.current_time(spec_full=True))
    print(TimeTool.current_time(spec_simple=True))
    # print(time.time()) # 1486793702.7263746
    print(TimeTool.format_time(timex=1486793702, format_spec='%Y/%m/%d // %H:%M'))
