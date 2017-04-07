# -*- coding: utf-8 -*-
# 2017/3/30

import asyncio
import json
import queue
import time
from multiprocessing import Queue, Process

import aiohttp
import requests

from spiderutils.copyheaders2dict import get_headers
from uc.codes.UcStore import UCstore

index_url = 'http://go.uc.cn/page/godcomment/shenpinglun'
# news_url = 'http://napi.uc.cn/3/classes/news_comments/categories/neirong/lists/617?_app_id=03b70b8484ae418789ebfec8ffa64820&_fetch=1&_max_age=1&_fetch_incrs=1&_size=10'
# next_news_url = 'http://napi.uc.cn/3/classes/news_comments/categories/neirong/lists/617?_app_id=03b70b8484ae418789ebfec8ffa64820&_fetch=1&_max_age=1&_fetch_incrs=1&_size=10&_max_pos={}'
news_url = 'http://napi.uc.cn/3/classes/news_comments/categories/neirong/lists/617'
next_news_url = 'http://napi.uc.cn/3/classes/news_comments/categories/neirong/lists/617'

headers1 = get_headers('headers.txt')
headers2 = get_headers('headers2.txt')


def news_data(max_pos='', size=10):
    return {
        '_app_id': '03b70b8484ae418789ebfec8ffa64820',
        '_fetch': '1',
        '_max_age': '1',
        '_fetch_incrs': '1',
        '_size': size,
        '_max_pos': max_pos
    }


def timestamp2date(timestamp):
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(str(timestamp)[:-3]))))


def strdate2timestamp(strdate):
    timeStamp = int(time.mktime(time.strptime(strdate, '%Y-%m-%dT%H:%M:%S.000+0800')))
    return timeStamp * 1000


def clear_mbody_url(url):
    splits = url.split('aid=')
    return splits[0] + 'aid=' + splits[1].split('&')[0]


store = UCstore()


def get_list_proc(q):
    resp = requests.get(news_url, headers=headers1, data=news_data())
    cont = json.loads(resp.text)
    for each in cont['data']:
        # store.insert(each)
        url = clear_mbody_url(each['link'])
        q.put(url)


def get_body_proc(q):
    start = time.time()
    urls = []
    while True:
        try:
            url = q.get(True, 10)
            urls.append(url)
            if len(urls) > 100:
                # get_body_req(urls)
                np = Process(target=get_body_req, args=(urls,))
                np.start()
                urls = []
        except queue.Empty:
            if len(urls) > 0:
                np = Process(target=get_body_req, args=(urls,))
                np.start()
            break
    end = time.time()
    print('cost {} second'.format(end - start - 3))


def get_body_req(urls):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_body_req_async(urls))


async def get_body_req_async(urls):
    tasks = [fetch_content(url) for url in urls]
    pages = await asyncio.gather(*tasks)
    for each in pages:
        print(each)


async def fetch_content(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers2) as resp:
            return await resp.text()


if __name__ == '__main__':
    m_body_queue = Queue()
    p1 = Process(target=get_list_proc, args=(m_body_queue,))
    p2 = Process(target=get_body_proc, args=(m_body_queue,))
    p1.start()
    p2.start()
