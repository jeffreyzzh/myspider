# -*- coding: utf-8 -*-
# 2016/11/10 0010
# JEFF

import requests
import urllib.request
import http.cookiejar
import http.cookies
import os


class WeiboSp(object):
    def __init__(self):
        self.start_url = "http://weibo.com/iamsotouched/home?wvr=5"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Host": "weibo.com",
            "Upgrade - Insecure - Requests": "1",
            "Cookie": self.get_cook()
        }

    def get_cook(self):
        with open('cookies.txt', 'r') as f:
            a = f.read()
        return a

    # cookjar = http.cookiejar.CookieJar()
    # cookjar_handle = urllib.request.HTTPCookieProcessor(cookiejar=cookjar)

    def domain(self):
        request = urllib.request.Request(self.start_url, headers=self.headers)
        response = urllib.request.urlopen(request)
        print(response)


if __name__ == '__main__':
    sp = WeiboSp()
    sp.domain()
