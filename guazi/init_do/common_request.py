# -*- coding: utf-8 -*-
# 2017/1/17

import requests
from guazi.tool.log import Logger

from guazi.settings import RequestSETTING
from guazi2.tool.ua import get_ua_dict as ua_header


class Request(object):
    def __init__(self):
        req_set = RequestSETTING()
        self.r_logger = Logger(req_set.request_logfile_name(), req_set.request_log_name()).get_logger()

    def get_headers(self):
        return ua_header()

    def get_page(self, url, proxy):
        try:
            resp = requests.get(url, headers=self.get_headers(), proxies=proxy, timeout=3)
        except Exception as e:
            self.r_logger.error(e)
        else:
            page_encode = resp.encoding
            return resp.content.decode(page_encode)


if __name__ == '__main__':
    r = Request()
    # html = r.get_page(url='https://www.guazi.com/gz/honda/', proxy=None)
    html = r.get_page(url='https://www.guazi.com/gz/honda/', proxy=None)
    print(html)
