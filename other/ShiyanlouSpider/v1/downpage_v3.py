# -*- coding: utf-8 -*-
# 2016/12/9

import os
import re
import urllib.parse as parse

import requests

from other.ShiyanlouSpider.v1.cookie2dict import MyCookie


class DownPage(object):
    def __init__(self):
        self.header = MyCookie().get_cook_dir()
        self.spider_url, self.base_path = self.init_dir()

    def init_dir(self):
        with open('downpage_v3_init.txt', 'r', encoding='utf-8') as f:
            start_url = f.read()
        html = self.get_page(start_url)
        print(html)
        title = re.search('<h4 class="pull-left course-infobox-title">(.*?)</h4>', html, re.S).group(1)
        title = re.search('<span>(.*?)</span>', title, re.S).group(1)
        print("title:{}".format(title))
        spider_url = re.search('<div class="pull-right lab-item-ctrl">(.*?)</div>', html, re.S).group(1)
        spider_url = re.search('href="(.*?)"', spider_url, re.S).group(1)
        print("spider_url:{}".format(spider_url))
        base_dir = r"C:\Users\Administrator\Desktop\{}".format(title)
        if not os.path.exists(base_dir):
            os.mkdir(base_dir)
            print('dir:{} init success...'.format(base_dir))
            os.mkdir(os.path.join(base_dir, 'js'))
            os.mkdir(os.path.join(base_dir, 'css'))
            os.mkdir(os.path.join(base_dir, 'img'))
        spider_url = parse.urljoin(start_url, spider_url)
        return spider_url, base_dir

    def get_page(self, url):
        print("get:url = {}".format(url))
        response = requests.get(url, headers=self.header)
        # print('response status code:{}'.format(response.status_code))
        return response.content.decode()

    def do_parse_html(self, html, page_count):
        js_count = 1
        js_list = re.findall('<script src="(.*?)"></script>', html, re.S)
        for js in js_list:
            with open(self.base_path + "\js\{}.js".format(js_count), 'wb') as f:
                f.write(requests.get(js).content)
            html = html.replace(js, 'js\{}.js'.format(js_count))
            js_count += 1

        css_count = 1
        css_list = re.findall('<link rel="stylesheet" href="(.*?)">', html, re.S)
        for css in css_list:
            with open(self.base_path + "\css\{}.css".format(css_count), 'wb')as f:
                f.write(requests.get(css).content)
            html = html.replace(css, 'css\{}.css'.format(css_count))
            css_count += 1

        # ![此处输入图片的描述](https://dn-anything-about-doc.qbox.me/document-uid8834labid1165timestamp1468333370769.png/wm)
        img_count = 1
        img_list = re.findall('!\[.*?\]\((.*?)\)', html, re.S)
        for img in img_list:
            with open(self.base_path + "img\{}.png".format(img_count), 'wb')as f:
                f.write(requests.get(img).content)
            html = html.replace(img, 'img\{}.png'.format(img_count))
            img_count += 1
        with open(self.base_path + '\{}.html'.format(page_count), 'w', encoding='utf-8') as f:
            f.write(html)

    def do_main(self, url, page_count):
        if url is None:
            url = self.spider_url
        if page_count is None:
            page_count = 1
        html = self.get_page(url)
        print('request sucess...')
        self.do_parse_html(html, page_count)
        page = re.search('<ul class="pager">(.*?)</ul>', html, re.S)
        print(page)
        next = re.search('<li class="next">(.*?)</li>', page, re.S)
        if next:
            next_page = re.search('<a href="(.*?)">', next.group(1), re.S).group(1)
            next_url = parse.urljoin(url, next_page)
            page_count += 1
            self.do_main(next_url, page_count)


if __name__ == '__main__':
    d = DownPage()
    d.do_main(None, None)
