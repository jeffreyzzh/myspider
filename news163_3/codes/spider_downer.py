# -*- coding: utf-8 -*-
# 2017/2/10

import requests

from news163_2.codes.spider_base import BaseClass


# URL下载器
class URLdowner(object):
    def __init__(self):
        self.logger = BaseClass.getlogger()

    def ajax_fetch(self, url):
        return self.fetch(url, 'gbk')

    def page_fetch(self, url):
        return self.fetch(url, 'utf-8')

    def fetch(self, url, encoding, counts=1):
        if counts >= 5:
            self.logger.error('{} crawl to many'.format(url))
            return None
        try:
            r = requests.get(url, timeout=3)  # 在这里抓取页面
            r.encoding = encoding
            if not r.status_code == 404:
                return r.text
            else:
                self.logger.error('url: {} 404 Not Found')
        except Exception as e:
            self.logger.error(e)
            return self.fetch(url, encoding, counts=counts + 1)


def getdowner():
    return URLdowner()


if __name__ == '__main__':
    u = URLdowner()
    cont = u.ajax_fetch('http://temp.163.com/special/00804KVA/cm_shehui.js')
    print(cont)
