# -*- coding: utf-8 -*-
# 2017/2/10

import time

from multiprocessing.dummy import Pool

from news163_2.tools.common_tools import TimeTool
from news163_2.codes.spider_base import BaseClass
from news163_2.codes.spider_datahandler import gethandler
from news163_2.codes.spider_manager import geturlmanager
from news163_2.codes.spider_parser import getparser

from news163_2.codes.spider_downer import getdowner


class News163Spider(object):
    def __init__(self):
        self.logger = BaseClass.getlogger()
        self.manager = geturlmanager()
        self.downer = getdowner()
        self.parser = getparser()
        self.handler = gethandler()

    def ajax_news(self):
        ajax_urls = self.manager.ajax_list_by_channel('shehui')
        pool = Pool()
        pool.map(self.dospider_ajax_url, ajax_urls)

    def dospider_ajax_url(self, url):
        cont = self.downer.ajax_fetch(url)
        jsons = self.parser.parse_ajax_channel(cont)
        for j in jsons:
            hot_url = self.manager.hotcomment_ajax_by_commenturl(j['commenturl'])
            comment = self.downer.page_fetch(hot_url)
            try:
                comment_dict = self.parser.parser_hotcomment(comment)
            except Exception as e:
                self.logger.error(e)
                self.logger.error('url: {} has a problem'.format(url))
            else:
                j['comment'] = comment_dict if comment_dict else None
            j['spider_time'] = TimeTool.current_time()
            self.handler.handler_ajax_new(new=j)


if __name__ == '__main__':
    start = time.time()

    n = News163Spider()
    n.ajax_news()

    print('{0:.6f}'.format(time.time() - start))
