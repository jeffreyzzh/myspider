# -*- coding: utf-8 -*-
# 2017/3/31

import json
import queue
from multiprocessing import Queue, Process
import time
from uc.spider_code import *
from uc.UcStore import UCstore

store = UCstore()


def main(q):
    pos = ''
    for i in range(1, 101):
        if i != 1:
            content = fetch_list(fet_url(pos))
        else:
            content = fetch_list(fet_url())
        if not content:
            break
        info = json.loads(content)
        if not info['data']:
            break
        store.insert_list(info['data'])
        [q.put({'link': each['link'], '_id': each['_id']}) for each in info['data']]
        pos = info['data'][-1]['_pos']


def gather_content(q):
    urls = []
    while True:
        try:
            url = q.get(timeout=5)
            urls.append(url['link'])
            if len(urls) >= 200:
                p0 = Process(target=fetch_zhengwen(urls))
                p0.start()
                urls = []
                time.sleep(10)
        except queue.Empty:
            if len(urls) > 0:
                p0 = Process(target=fetch_zhengwen(urls))
                p0.start()
            break


if __name__ == '__main__':
    q = Queue()
    main(q)
    p = Process(target=gather_content, args=(q,))
    p.start()
