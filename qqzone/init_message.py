# -*- coding: utf-8 -*-
# 2016/12/2

import datetime
import pymongo

class InitMessage(object):
    def __init__(self):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
            'Referer': 'http://ctc.qzs.qq.com/qzone/newblog/blogcanvas.html'
        }
        self.db = pymongo.MongoClient['QQ']