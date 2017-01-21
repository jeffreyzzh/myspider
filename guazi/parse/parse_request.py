# -*- coding: utf-8 -*-
# 2017/1/18 0018
# JEFF

import requests
from guazi.tool.log import Logger

import guazi.proxy.proxy_handle as p_h
from guazi.settings import RequestSETTING, EXCEPTIONINFO
from guazi2.tool.ua import get_ua_dict


def requesturl(url):
    resp = requests.get(url)
    resp.encoding = 'utf-8'
    return resp.text


class Request(object):
    def __init__(self):
        self.timeout = RequestSETTING.request_timeout()
        self.counts = RequestSETTING.request_counts()
        self.logger = Logger(RequestSETTING.request_logfile_name(), RequestSETTING.request_log_name()).get_logger()
        p_h.init_proxypool()

    def do_getpage(self, url, count=1):
        if count == self.counts:
            self.logger.error(EXCEPTIONINFO.false_count_info())
            return None
        proxy = p_h.get_one_proxy()
        try:
            resp = requests.get(url, headers=get_ua_dict(), proxies=proxy, timeout=self.timeout)
            resp.encoding = 'utf-8'
            self.logger.info('{} ok'.format(proxy))
            return resp.text
        except Exception as e:
            p_h.mark_unuse_ip(proxy)
            p_h.delete_ip_ondb()
            self.logger.debug(e)
            self.logger.debug(EXCEPTIONINFO.request_false_info())
            self.do_getpage(url=url, count=count + 1)


if __name__ == '__main__':
    q = Request()
    for i in range(30):
        html = q.do_getpage('https://www.guazi.com/gz/dazhong/')
