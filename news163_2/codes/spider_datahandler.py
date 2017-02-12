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
        self.coll = db[
            settings.COLLECTNAME.format(
                TimeTool.format_time(format_spec=settings.MONGO_USE_DATE_SPECS)
            )
        ]

    def handler_ajax_new(self, new):
        if not new or not isinstance(new, dict):
            print('false')
        self.coll.insert(new)
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
