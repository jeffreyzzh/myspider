# -*- coding: utf-8 -*-
# 2016/12/21 0021
# JEFF

import os
import re
import requests
import time
import lxml.html

spider_list = [
    'http://club.autohome.com.cn/bbs/thread-c-3207-58916494-1.html#pvareaid=100702'
]


class ImgDown(object):
    def __init__(self):
        self.timeout = 5
        self.re_img = re.compile('src="http://club2.autoimg.cn/album/g(.*?)\.jpg', re.S)
        self.re_img2 = re.compile('src9="(.*?)"', re.S)
        self.base_dir = self.init_dir()

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
        # self.down_source_at_desktop(title.group(1), html.text)
        if title:
            title_name = title.group(1)
            print(title_name)
        all_img = re.findall(self.re_img, html.text)
        new_all = ['http://club2.autoimg.cn/album/g' + img + '.jpg' for img in all_img]
        all_img2 = re.findall(self.re_img2, html.text)
        new_all.extend(all_img2)

        img_count = 1
        img_name = self.base_dir + '\\' + "{}.jpg"

        for img in new_all:
            filename = img_name.format(img_count)
            with open(filename, 'wb') as f:
                f.write(requests.get(img).content)
            print('spider {} success'.format(img))
            img_count += 1

    def do_main2(self):
        html = requests.get(spider_list.pop()).text
        selector = lxml.html.fromstring(html)
        all_img = selector.xpath('//img')
        print(len(all_img))

    def init_dir(self):
        desktop = os.path.join(os.path.expanduser("~"), 'Desktop')
        title = '汽车之家{}'.format(time.strftime('%Y-%m-%d'))
        base_dir = os.path.join(desktop, title)
        if not os.path.exists(base_dir):
            os.mkdir(base_dir)
        return base_dir


if __name__ == '__main__':
    d = ImgDown()
    start_time = time.time()
    d.do_main2()
    print('spider consumes for {} seconds'.format(time.time() - start_time))
