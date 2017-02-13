# -*- coding: utf-8 -*-
# 2017/2/11 0011
# JEFF

import pymongo
from news163_2.codes.spider_base import BaseClass
from news163_2.tools.common_tools import TimeTool, DbTool
from news163_2 import settings


class Darahandler(object):
    def __init__(self):
        self.logger = BaseClass.getlogger()
        self.shehui_coll = DbTool.get_mongocoll_by_channel('shehui')
        self.guoji_coll = DbTool.get_mongocoll_by_channel('guoji')
        self.guonei_coll = DbTool.get_mongocoll_by_channel('guonei')
        self.other_coll = DbTool.get_mongocoll_by_channel('other')
        self.coll_dict = self.init_colls()

    def init_colls(self):
        mongo_colls = dict()
        for i in settings.CHANNEL_LIST:
            mongo_colls[i] = DbTool.get_mongocoll_by_channel(i)
        return mongo_colls

    def handler_ajax_new(self, new):
        if not new or not isinstance(new, dict):
            print('false')
        channelname = new.get('channelname')
        channel_coll = self.coll_dict.get(channelname)
        if channel_coll:
            channel_coll.insert(new)
        else:
            self.other_coll.insert(new)
        self.logger.info('mongodb insert {}'.format(new))


def gethandler():
    return Darahandler()


if __name__ == '__main__':
    dh = Darahandler()
    d = dh.init_colls()
    for k, v in d.items():
        print(k)
        print(v.find().count())
