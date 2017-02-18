# -*- coding: utf-8 -*-
# 2017/2/11 0011
# JEFF

import pymongo
import sys

from news163_2.codes.spider_base import BaseClass
from news163_2.tools.common_tools import TimeTool, DbTool
from news163_2 import settings


class Datahandler(object):
    def __init__(self, host='localhost', port=27017, dbname='163news'):
        self.logger = BaseClass.getlogger()
        client = pymongo.MongoClient(host=host, port=port)
        db = client[dbname]
        self.shehui = db['shehui_coll']
        self.guoji = db['guoji_coll']
        self.guonei = db['guonei_coll']
        self.sport = db['sport_coll']
        self.ent = db['ent_coll']
        self.money = db['money_coll']
        self.tech = db['tech_coll']
        self.lady = db['lady_coll']
        self.edu = db['edu_coll']
        self.coll = {
            'shehui': self.shehui,
            'guoji': self.guoji,
            'guonei': self.guonei,
            'sport': self.sport,
            'ent': self.ent,
            'money': self.money,
            'tech': self.tech,
            'lady': self.lady,
            'edu': self.edu,
        }

    def handler_ajax_new(self, new):
        if not new or not isinstance(new, dict):
            sys.stdout.write('data is empty')
            sys.stdout.flush()
        channelname = new.get('channelname')
        self.coll.get(channelname).insert(new)

    def test_read(self, coll):
        for i in coll.find().limit(100):
            print(i)


def gethandler():
    return Datahandler()


if __name__ == '__main__':
    dh = Datahandler()
    dh.test_read(dh.shehui)
