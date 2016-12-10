# -*- coding: utf-8 -*-
# 2016/12/6

from other.test.cookie2dict import MyCookie
from bs4 import BeautifulSoup
import requests


class Shiyanlou(object):
    def __init__(self):
        self.header = MyCookie().get_cook_dir()
        self.timeout = 10

    def do_request(self, url):
        response = requests.get(url=url, headers=self.header, timeout=self.timeout)
        if 100 > response.status_code or response.status_code > 400:
            return None
        soup = BeautifulSoup(response.text, 'lxml')
        return soup.prettify()

    def down_page(self, html):
        if html is None:
            print('no page')
        with open('1.html', 'w', encoding='utf-8') as f:
            f.write(html)


if __name__ == '__main__':
    s = Shiyanlou()
    html = s.do_request('https://www.shiyanlou.com/courses/707/labs/2300/document')
    if html:
        s.down_page(html)
