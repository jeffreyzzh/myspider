# -*- coding: utf-8 -*-
# 2017/2/10

import requests

from news163_2.spider_logger import getlogger


# URL下载器
class URLdowner(object):
    def __init__(self):
        self.logger = getlogger()

    def ajax_fetch(self, url):
        return self.fetch(url, 'gbk')

    def page_fetch(self, url):
        return self.fetch(url, 'utf-8')

    def fetch(self, url, encoding):
        self.logger.info(url)
        try:
            r = requests.get(url, timeout=3)  # 在这里抓取页面
            r.encoding = encoding
            if not r.status_code == 404:
                return r.text
            else:
                self.logger.error('url: {} 404 Not Found')
        except Exception as e:
            self.logger.error(e)
            return None


def getdowner():
    return URLdowner()


if __name__ == '__main__':
    u = URLdowner()
    u.logger.error(123)
