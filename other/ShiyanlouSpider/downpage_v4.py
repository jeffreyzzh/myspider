# -*- coding: utf-8 -*-
# 2016/12/11 0011
# JEFF
import os
import random
import re
import time

import redis
import requests
from other.ShiyanlouSpider.downpage_util import format_print
from other.ShiyanlouSpider.downpage_util import get_header
from other.ShiyanlouSpider import downpage_param
from multiprocessing.dummy import Pool as d_pool
from requests import Session


class DownPage(object):
    def __init__(self):
        self.session = Session()
        self.timeout = 10
        start_url = 'https://www.shiyanlou.com/login'
        response = self.session.get(start_url).content
        html = response.decode()
        account = input("account:")
        password = input("password:")
        csrf = re.search('<input id="csrf_token" name="csrf_token" type="hidden" value="(.*?)">', html, re.S)
        csrf_token = csrf.group(1)
        data = {
            'csrf_token': csrf_token,
            'next': None,
            'login': account,
            'password': password,
            'submit': '进入实验楼'
        }
        response = self.session.post(start_url, data=data)
        resp_url = response.url
        if start_url in resp_url:
            format_print("login defeated")
        if response.status_code == 200:
            format_print('code:{}, {}'.format(response.status_code, 'login success'))

    def get_page(self, url):
        second = random.randint(3, 8)
        print("get url -----> {}".format(url))
        print("spider sleep {} s".format(second))
        print()
        time.sleep(second)
        return self.session.get(url=url, headers=get_header()).content.decode()

    # 抓取每个课程之前的初始化方法
    def do_init_of_course(self, url):
        html = self.get_page(url)
        # 标题
        title = re.search('<h4 class="pull-left course-infobox-title">(.*?)</h4>', html, re.S).group(1)
        title = re.search('<span>(.*?)</span>', title, re.S).group(1)
        title = title.replace('/', ' ').replace('\\', ' ')
        format_print("the title of course:  {} ".format(title), title)
        base_dir = r"C:\Users\Administrator\Desktop\{}".format(title)
        # 实际课程的URL
        spider_url = re.search('<div class="pull-right lab-item-ctrl">(.*?)</div>', html, re.S).group(1)
        spider_url = re.search('href="(.*?)"', spider_url, re.S).group(1)
        if not os.path.exists(base_dir):
            os.mkdir(base_dir)
        format_print('dir:{} init success...'.format(base_dir), title)
        js_path = os.path.join(base_dir, 'js')
        if not os.path.exists(js_path):
            os.mkdir(js_path)
        css_path = os.path.join(base_dir, 'css')
        if not os.path.exists(css_path):
            os.mkdir(css_path)
        img_path = os.path.join(base_dir, 'img')
        if not os.path.exists(img_path):
            os.mkdir(img_path)
        # / courses / 705 / labs / 2299 / document
        # https: // www.shiyanlou.com / courses / 705 / labs / 2299 / document
        # 完整URL
        full_url = 'http://www.shiyanlou.com{}'.format(spider_url)
        # print("spider_url:{}".format(full_url))
        return full_url, base_dir, title

    # 解析下载课程
    def do_parse(self, url, base_dir, title, js_count, css_count, img_count, do_count):
        format_print('down course\' page {}'.format(do_count), title)
        html = self.get_page(url)
        # print(html)
        print('down -----> js')
        js_list = re.findall('<script src="(.*?)"></script>', html, re.S)
        for js in js_list:
            with open(base_dir + "\js\{}.js".format(js_count), 'wb') as f:
                f.write(requests.get(js).content)
            html = html.replace(js, 'js\{}.js'.format(js_count))
            js_count += 1

        print('down -----> css')
        css_list = re.findall('<link rel="stylesheet" href="(.*?)">', html, re.S)
        for css in css_list:
            with open(base_dir + "\css\{}.css".format(css_count), 'wb')as f:
                f.write(requests.get(css).content)
            html = html.replace(css, 'css\{}.css'.format(css_count))
            css_count += 1

        print('down -----> img')
        img_list = re.findall('!\[.*?\]\((.*?)\)', html, re.S)
        for img in img_list:
            print(img)
            with open(base_dir + "\img\{}.png".format(img_count), 'wb')as f:
                f.write(requests.get(img).content)
            html = html.replace(img, 'img\{}.png'.format(img_count))
            img_count += 1

        page = re.search('<ul class="pager">(.*?)</ul>', html, re.S)
        before_c = re.search('<li class="previous">(.*?)</li>', page.group(), re.S)
        next_c = re.search('<li class="next">(.*?)</li>', page.group(), re.S)
        next_url = ''
        if before_c:
            before_page = re.search('<a href="(.*?)">', before_c.group(1), re.S).group(1)
            # before_url = 'http://www.shiyanlou.com{}'.format(before_page)
            html = html.replace(before_page, '{}.html'.format(do_count - 1))
        if next_c:
            next_page = re.search('<a href="(.*?)">', next_c.group(1), re.S).group(1)
            next_url = 'http://www.shiyanlou.com{}'.format(next_page)
            html = html.replace(next_page, '{}.html'.format(do_count + 1))

        with open(base_dir + '\{}.html'.format(do_count), 'w', encoding='utf-8') as f:
            f.write(html)
        format_print('course page {} is down success'.format(do_count), title)

        do_count += 1
        if next_c:
            self.do_parse(next_url, base_dir, js_count, css_count, img_count, do_count, title)

    def do_execute(self, url):
        real_url, base_dir, title = self.do_init_of_course(url)
        format_print('down course start   down course start   down course start', title)
        self.do_parse(real_url, base_dir, title, 1, 1, 1, 1)
        format_print(' down course end     down course end     down course end ', title)

    def do_main(self):
        # v1.4.1
        # 单个URL
        # start_url = downpage_param.get_spider_url()
        # real_url, base_dir = self.do_init_of_course(start_url)
        # self.do_parse(real_url, base_dir, 1, 1, 1, 1)

        # v 1.4.2
        # 多个URL
        url_list = downpage_param.get_spider_list()
        for url in url_list:
            self.do_execute(url)

            # v 1.4.3
            # 多个URL，多线程
            # url_list = downpage_param.get_spider_list()
            # pool = d_pool(4)
            # pool.map(self.do_execute, url_list)

            # v 1.4.4
            # 多个URL，多线程，redis队列
            # r = redis.Redis()
            # queue = 'shiyanlou_spider'
            #
            # url_list = []
            # while True:
            #     i = r.spop(queue)
            #     if i is None:
            #         break
            #     url = i.decode()
            #     print(url)
            #     url_list.append(url)
            # pool = d_pool(4)
            # pool.map(self.do_execute, url_list)


if __name__ == '__main__':
    d = DownPage()
    start_time = time.time()
    d.do_main()
    format_print('spider consumes for {} seconds'.format(time.time() - start_time))
