# -*- coding: utf-8 -*-
# 2016/12/21 0021
# JEFF
import time

import re
import requests

spider_list = [
    'http://club.autohome.com.cn/bbs/thread-c-3207-58916494-1.html#pvareaid=100702'
]


class ImgDown(object):
    def __init__(self):
        self.timeout = 5
        self.re_img = re.compile('src="http://club2.autoimg.cn/album/g22/(.*?)\.jpg', re.S)

    def do_request(self, url, count=3):
        if count == 0:
            return None
        try:
            response = requests.get(url, timeout=self.timeout)
            return response.content.decode()
        except requests.exceptions.ConnectTimeout:
            print("time out!!")
            print(count)
            self.do_request(url, count=count - 1)
        except Exception:
            print("program error")
            return None

    def do_main(self):
        html = requests.get(spider_list.pop())
        # print(html)
        title = re.search('<title>(.*?)</title>', html.text, re.S)
        if title:
            title_name = title.group(1)
            print(title_name)
        all_img = re.findall(self.re_img, html.text)
        new_all = ['http://club2.autoimg.cn/album/g22/' + img + '.jpg' for img in all_img]
        for img in new_all:
            print(img)

    def init_dir(self, title):
        pass


if __name__ == '__main__':
    d = ImgDown()
    start_time = time.time()
    d.do_main()
    print('spider consumes for {} seconds'.format(time.time() - start_time))
