# -*- coding: utf-8 -*-
# 2016/12/16 0016
# JEFF

from http.cookiejar import CookieJar
from urllib import request
from urllib.request import ProxyHandler
from urllib.request import HTTPCookieProcessor
from urllib.request import build_opener
from urllib.request import Request
from urllib.request import urlopen
import hashlib

from other.JianDan.core.headers import make_headers
from other.JianDan.core.cache import DiskCache, CacheKeyNotExistError
from other.JianDan.core.proxy import Proxy


def build_fetch(use_cache=False, timeout=5, use_cookie=False, proxy=None, mobile=None):
    """
    build fetch fucntion with proxy
    :param use_cache:
    :param timeout:
    :param use_cookie:
    :param proxy:
    :param mobile:
    :return:
    """
    if use_cookie:
        cookie_handler = HTTPCookieProcessor(CookieJar())
    else:
        cookie_handler = None

    if proxy and isinstance(proxy, Proxy):
        proxy_handler = ProxyHandler({'http': proxy.assemble()})
    else:
        proxy_handler = None

    handlers = [cookie_handler, proxy_handler]
    handlers = filter(lambda x: x, handlers)

    opener = build_opener(*handlers)

    if use_cache:
        cache = DiskCache()

    def fetch(url):
        if use_cache:
            key = hashlib.md5(url).hexdigest()
            try:
                return cache.get(url)
            except CacheKeyNotExistError:
                pass

        req = Request(url, headers=make_headers(mobile=mobile))
        response = opener.open(req, timeout=timeout)
        content = response.read()

        if use_cache:
            cache.set(key, content)
        return content

    return fetch
