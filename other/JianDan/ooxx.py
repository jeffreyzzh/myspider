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
        pass
