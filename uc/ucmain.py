# -*- coding: utf-8 -*-
# 2017/3/30

import requests
import json
import time
from spiderutils.copyheaders2dict import get_headers
from uc.UcStore import UCstore
from multiprocessing import Queue, Process
# from threading import Thread

import queue

index_url = 'http://go.uc.cn/page/godcomment/shenpinglun'
news_url = 'http://napi.uc.cn/3/classes/news_comments/categories/neirong/lists/617?_app_id=03b70b8484ae418789ebfec8ffa64820&_fetch=1&_max_age=1&_fetch_incrs=1&_size=10'
next_news_url = 'http://napi.uc.cn/3/classes/news_comments/categories/neirong/lists/617?_app_id=03b70b8484ae418789ebfec8ffa64820&_fetch=1&_max_age=1&_fetch_incrs=1&_size=10&_max_pos={}'

headers1 = get_headers('headers.txt')
headers2 = get_headers('headers2.txt')


def news_data(max_pos=''):
    return {
        '_app_id': '03b70b8484ae418789ebfec8ffa64820',
        '_fetch': '1',
        '_max_age': '1',
        '_fetch_incrs': '1',
        '_size': '',
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
    tasks = []
    while True:
        try:
            url = q.get(True, 3)
            tasks.append(url)
            if len(tasks) > 200:
                p = Process(target=get_body_req, args=(tasks,))
                p.start()
        except queue.Empty:
            if len(tasks) > 0:
                p = Process(target=get_body_req, args=(tasks,))
                p.start()
            break
    end = time.time()
    print('cost {} second'.format(end - start - 3))


def get_body_req(tasks):
    for each in tasks:
        resp = requests.get(each, headers=headers2)
        print(resp.status_code)


if __name__ == '__main__':
    m_body_queue = Queue()
    p1 = Process(target=get_list_proc, args=(m_body_queue,))
    p2 = Process(target=get_body_proc, args=(m_body_queue,))
    p1.start()
    p2.start()
