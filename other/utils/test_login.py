# -*- coding: utf-8 -*-
# 2016/12/5 0005
# JEFF

import requests
from selenium import webdriver
from other.utils.cookie2dict import MyCookie


class DoDownload(object):
    def __init__(self):
        # self.start_url = 'http://www.zhihu.com'
        self.start_url = 'https://www.shiyanlou.com/courses/696/labs/2287/document'
        print('hello')

    def do_main(self):
        html = self.do_down()
        print(html.decode())


if __name__ == '__main__':
    d = DoDownload()

    c = MyCookie()
    cookie = c.get_cook_dir()
    print(cookie)

    driver = webdriver.Chrome()
    driver.add_cookie(cookie)

    driver.get_cookies()
    #
    # driver.get('https://www.shiyanlou.com/courses/696/labs/2287/document')
