# -*- coding: utf-8 -*-
# 2017/2/11 0011
# JEFF

import pymongo
from news163_2.codes.spider_base import BaseClass
from news163_2.tools.common_tools import TimeTool
from news163_2 import settings


class Darahandler(object):
    def __init__(self):
        self.logger = BaseClass.getlogger()
        client = pymongo.MongoClient()
        db = client[settings.MONGODBNAME]
        self.shehui_coll = db[settings.COLLECTNAME.format('shehui')]
        self.guoji_coll = db[settings.COLLECTNAME.format('guoji')]
        self.guonei_coll = db[settings.COLLECTNAME.format('guonei')]
        self.other_coll = db[settings.COLLECTNAME.format('other')]

    def handler_ajax_new(self, new):
        if not new or not isinstance(new, dict):
            print('false')
        channelname = new.get('channelname')
        if channelname == 'shehui':
            self.shehui_coll.insert(new)
        elif channelname == 'guoji':
            self.guoji_coll.insert(new)
        elif channelname == 'guonei':
            self.guonei_coll.insert(new)
        else:
            self.other_coll.insert(new)
        self.logger.info('mongodb insert {}'.format(new))


def gethandler():
    return Darahandler()


if __name__ == '__main__':
    dh = Darahandler()
    dh.handler_ajax_new(
        {
            'name': 'jeffrey',
            'age': 25
        }
    )
