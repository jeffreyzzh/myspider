# -*- coding: utf-8 -*-
# 2017/1/21

import requests
import json
from guazi2.tool.ua import get_ua_dict
from guazi2.tool.log import Logger
from guazi2.tool.time_tool import log_current_date


class GuaziRequest(object):
    def __init__(self):
        self.logger = Logger('{}.log'.format(log_current_date()), 'guazi').get_logger()

    def get_one_proxy(self):
        r = requests.get('http://127.0.0.1:8000/?types=0&count=1')
        ip_ports = json.loads(r.text)
        for uip in ip_ports:
            ip_dict = {
                'http': 'http://{}:{}'.format(uip[0], uip[1]),
                'https': 'https://{}:{}'.format(uip[0], uip[1])
            }
            return ip_dict

    def do_requests(self, url, count=1):
        if count >= 5:
            self.logger.error('{} to much error...'.format(url))
            return None
        try:
            resp = requests.get(url, proxies=self.get_one_proxy(), headers=get_ua_dict(), timeout=5)
            resp.encoding = 'utf-8'
            return resp.text
        except Exception as e:
            self.logger.error(e)
            self.do_requests(url, count=count + 1)


if __name__ == '__main__':
    pass
