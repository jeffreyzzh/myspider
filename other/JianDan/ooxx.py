# -*- coding: utf-8 -*-
# 2016/12/15

import os
import re
import sys
import socket
from urllib.error import URLError, HTTPError

from other.JianDan.core.proxy import MimiProxyFinder, ProxyPool
from other.JianDan.core.fetch import build_fetch
from other.JianDan.core.cache import CacheKeyNotExistError, DiskCache

OOXX_URL = 'https://jiandan.net/ooxx'
TIMEOUT = 5
FAILE_COUNT = 0


class Page:
    count = 0
    regexes = {
        'count': re.compile(r'<span class="current-comment-page">\[(\d+)\]</span>', re.MULTILINE),
        'image_section': re.compile(r'<li id="comment-\d+">[\s\S]*?</li>', re.MULTILINE),
        'image_url': re.compile(r'(https?://ww.*?)" target="_blank" class="view_img_link">'),
        'image_number': re.compile(r'<a href="https?://jandan.net/ooxx/page-\d+?#comment-\d+?">(\d+?)</a>'),
    }

    @classmethod
    def get_count(cls, proxy):
        """
        return how many pages we have

        :param proxy:
        :return:
        """

        fetch = build_fetch(proxy=proxy)
        front_page = fetch(OOXX_URL)
        cls.count = int(cls.regexes['count'].findall(front_page)[0])

    def __init__(self, page_number, fetch=None):
        self.number = page_number
        self.fetch = fetch

    def fetch_images(self):
        images = []
        url = '{}.page-{}'.format(OOXX_URL, self.number)
        print('fetch image at : ' + url)
        try:
            html = self.fetch(url)
        except IOError:
            return images
        image_sections = self.regexes['image_section'].findall(html)
        print('find image sections ' + str(len(image_sections)))
        for image_section in image_sections:
            try:
                url = self.regexes['image_url'].findall(image_section)[0]
                number = self.regexes['image_number'].findall(image_section)[0]
            except IndexError:
                continue
                images.append(Image(number, url))
        print('find images: ' + str(len(images)))
        return images


class Image:
    desktop = os.path.join(os.path.expanduser("~"), 'Desktop')
    folder = 'images'
    img_dir = os.path.join(folder, folder)

    def __int__(self, number, url):
        self.number = number
        self.url = url
        if not os.path.exists(self.img_dir):
            os.mkdir(self.img_dir)

    def download(self, fetch):
        extname = os.path.splitext(self.url)[1]
        filename = os.path.join(self.img_dir, self.number + extname)
        print('downing: ' + self.number + extname)
        with open(filename, 'wb') as f:
            try:
                f.write(fetch(self.url))
            except IOError:
                print('{} download failed'.format(self.number))


def crawl(start=1):
    fail_count = 0
    proxy_finder = MimiProxyFinder()
    proxy_pool = ProxyPool(finder=proxy_finder)
    proxy_pool.refresh()
    Page.get_count(proxy_pool.random_proxy())
    print('we got {} pages to crawl'.format(Page.count))

    for i in range(start, Page.count):
        cached_fetch = build_fetch(use_cache=True, use_cookie=True, proxy=proxy_pool.random_proxy())
        uncached_fetch = build_fetch()
        page = Page(i, fetch=cached_fetch)
        images = page.fetch_images()
        if not images:
            fail_count += 1
        if fail_count == 2:
            print('too many failures, refreshing proxy pool')
            proxy_pool.refresh()
        for image in images:
            try:
                image.download(fetch=uncached_fetch)
            except IOError:
                pass


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage python {} crawl start".format(sys.argv[0]))
    else:
        if sys.argv[1] == 'crawl':
            try:
                start = int(sys.argv[2])
            except ValueError:
                start = 0
            crawl(start)
