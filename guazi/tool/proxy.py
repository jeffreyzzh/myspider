# -*- coding: utf-8 -*-
# 2017/1/17
# author = JEFF

import requests


class DefaultProxy(object):
    def __init__(self):
        self.get_url = 'http://127.0.0.1:8000'
        self.del_url = 'http://127.0.0.1:8000'

    def get_proxy(self):
        return requests.get(self.get_url).text

    def delete_proxy(self):
        requests.delete(self.del_url)
