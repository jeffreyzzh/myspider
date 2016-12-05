# -*- coding: utf-8 -*-
# 2016/12/5 0005
# JEFF

import requests


class DoDownload(object):
    def __init__(self):
        self.cookie_str = self.do_init()
        # self.start_url = 'http://www.zhihu.com'
        self.start_url = 'https://www.shiyanlou.com/courses/696/labs/2287/document'

    def do_init(self):
        with open('cookie_t.txt', 'r') as f:
            c = f.read()
        return c

    def do_down(self):
        session = requests.Session()
        cookie = {
            'Cookie': self.cookie_str
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
            'Referer': 'https://www.shiyanlou.com/courses/696',
            'Upgrade-Insecure-Requests': '1',
            'Connection': 'keep-alive'
        }
        return session.get(self.start_url, cookies=cookie, headers=headers).content

    def do_main(self):
        html = self.do_down()
        print(html.decode())


if __name__ == '__main__':
    d = DoDownload()
    d.do_main()
