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
        ajax_urls = self.manager.ajax_list_by_channel('guonei')
        pool = Pool()
        pool.map(self.dospider_ajax_url, ajax_urls)

    def dospider_ajax_url(self, url):
        cont = self.downer.ajax_fetch(url)
        jsons = self.parser.parse_ajax_channel(cont)
        channelname = jsons[0].get('channelname')
        filter_list = self.manager.commenturl_filterlist_by_channel(channelname)
        for j in jsons:
            # 对要进行的URL进行过滤去重
            commenturl = j['commenturl']
            if commenturl not in filter_list:
                self.handler_commenturl(commenturl=commenturl, j=j)

    def handler_commenturl(self, commenturl, j):
        hot_url = self.manager.hotcomment_ajax_by_commenturl(commenturl)
        comment = self.downer.page_fetch(hot_url)
        comment_dict = self.parser.parser_hotcomment(comment, hot_url)
        j['comment'] = comment_dict if comment_dict else None
        j['spider_time'] = TimeTool.current_time()
        self.handler.handler_ajax_new(new=j)


if __name__ == '__main__':
    start = time.time()

    n = News163Spider()
    n.ajax_news()

    print('{0:.6f}'.format(time.time() - start))
