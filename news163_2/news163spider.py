# -*- coding: utf-8 -*-
# 2017/2/10

import json
import re
import time

from news163_2.spider_downer import getdowner
from news163_2.spider_logger import getlogger


class News163Spider(object):
    def __init__(self):
        self.logger = getlogger()
        self.downer = getdowner()

    regex_dict = {
        'cont': re.compile('(\[.*\])', re.S),
        'titles': re.compile('"title":"(.*?)"', re.S),
        'docurls': re.compile('"docurl":"(.*?)"', re.S),
        'commenturls': re.compile('"commenturl":"(.*?)"', re.S),
        'timeums': re.compile('"tienum":(.*?),', re.S),
        'tlinks': re.compile('"tlink":"(.*?)"', re.S),
        'labels': re.compile('"label":"(.*?)"', re.S),
        'o_keywords': re.compile('"keywords":\[\s*(.*?)\s*\],', re.S),
        'times': re.compile('"time":"(.*?)"', re.S),
        'newstypes': re.compile('"newstype":"(.*?)"', re.S),
        'channelnames': re.compile('"channelname":"(.*?)"', re.S)
    }

    URL = 'http://news.163.com/shehui/'
    AJAX_URL = 'http://temp.163.com/special/00804KVA/cm_{}.js'
    AJAX_URLS = 'http://temp.163.com/special/00804KVA/cm_{}_0{}.js'
    HOT_COMMENT_URL = 'http://comment.news.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/{}/comments/hotList?limit=20'

    def ajax_list(self, channel='shehui'):
        urls = []
        urls.append(self.AJAX_URL.format(channel))
        for i in range(2, 9):
            urls.append(self.AJAX_URLS.format(channel, i))
        return urls

    def fetch_ajax_by_channel(self, channel='shehui'):
        spider_lists = self.ajax_list(channel)
        return spider_lists


if __name__ == '__main__':
    start = time.time()

    n = News163Spider()
    for i in n.fetch_ajax_by_channel('guoji'):
        cont = n.downer.ajax_fetch(i)
        print(cont)

    print('{0:.6f}'.format(time.time() - start))
