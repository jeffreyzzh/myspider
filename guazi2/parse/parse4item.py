# -*- coding: utf-8 -*-
# 2017/1/23 0023
# JEFF

import random
import time
from guazi2.db.common_getset_info import GetAndSet
from guazi2.parse.parse_requests import GuaziRequest
from guazi2.tool.log import logger
from urllib.parse import urljoin
import lxml.html
import queue


class GuaziItemParse(object):
    def __init__(self, isproxy=True):
        self.isproxy = isproxy
        self.logger = logger
        self.request = GuaziRequest(isproxy=self.isproxy)
        self.queue = queue.Queue()
        self.xpath_expression = ''
        gs = GetAndSet()
        self.item_coll = gs.get_mongo_dayitems()
        self.url_coll = gs.get_mongo_dayurls()

    def init_spider_list(self):
        urls = self.url_coll.find()
        for u in urls:
            print(u)


if __name__ == '__main__':
    gp = GuaziItemParse()
    gp.init_spider_list()
