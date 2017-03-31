# -*- coding: utf-8 -*-
# 2017/3/31

import aiohttp
import asyncio
import requests
from spiderutils.copyheaders2dict import get_headers

list_headers = get_headers('headers.txt')
zw_headers = get_headers('headers2.txt')

ajax_url = 'http://napi.uc.cn/3/classes/news_comments/categories/neirong/lists/617?_app_id=03b70b8484ae418789ebfec8ffa64820&_fetch=1&_max_age=1&_fetch_incrs=1&_size=200'
page_url = 'http://napi.uc.cn/3/classes/news_comments/categories/neirong/lists/617?_app_id=03b70b8484ae418789ebfec8ffa64820&_fetch=1&_max_age=1&_fetch_incrs=1&_size=200&_max_pos={}'


def fet_url(pos=''):
    return page_url.format(pos)


def fetch(url, headers, data):
    error_count = 0
    try:
        resp = requests.get(url, headers=headers, data=data, timeout=3)
        if resp.status_code != 200:
            print(1)
            return None
        return resp.text
    except Exception as e:
        error_count += 1
        print(e)
        print('error url {}'.format(url))
        print('error count {}'.format(error_count))
        if error_count >= 5:
            print('to many error, next...')
        return fetch(url, headers, data=data)


def fetch_list(url):
    return fetch(url, headers=list_headers, data=None)


def fetch_zhengwen(urls):
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(get_body_req_async(urls))
    print(len(urls))
    # for u in urls:
    #     print(u)
