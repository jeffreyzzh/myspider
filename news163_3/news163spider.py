# -*- coding: utf-8 -*-
# 2017/2/10

import time

from multiprocessing.dummy import Pool
from news163_2 import settings
from news163_2.tools.common_tools import TimeTool
from news163_2.codes.spider_base import BaseClass
from news163_2.codes.spider_datahandler import gethandler
from news163_2.codes.spider_manager import geturlmanager
from news163_2.codes.spider_parser import getparser
from news163_2.codes.spider_downer import getdowner


class News163Spider(object):
    def __init__(self, thread_num, hotcomment_num=40, newcomment_num=10, crawl_channels=settings.CHANNEL_LIST):
        self.thread_num = thread_num
        self.hotcomment_num = hotcomment_num
        self.newcomment_num = newcomment_num
        self.crawl_channels = crawl_channels

    # self.logger = BaseClass.getlogger()
    # self.manager = geturlmanager()
    # self.downer = getdowner()
    # self.parser = getparser()
    # self.handler = gethandler()

    def domain(self):
        pass


if __name__ == '__main__':
    start = time.time()

    n = News163Spider()
    n.domain()

    print('{0:.6f}'.format(time.time() - start))
