# -*- coding: utf-8 -*-
# 2017/4/7

import json
import queue
import random
from multiprocessing import Queue, Process

from uc.codes.spider_code import *


def crawl_run(dbpos, q):
    pos = ''
    full_crawl_list = []
    for i in range(1, 101):
        if i != 1:
            content = fetch_list(fet_url(pos))
        else:
            content = fetch_list(fet_url())
        if not content:
            print('没有返回数据，停止采集')
            break
        info = json.loads(content)
        if not info['data']:
            print('没有请求数据，停止采集')
            break
        crawl_list, pos = handle_crawl_data(info['data'], dbpos, q)
        full_crawl_list.extend(crawl_list)
        if pos <= dbpos:
            print('停止采集')
            break
    logger.info('本次采集新闻数: {}'.format(len(full_crawl_list)))
    return full_crawl_list


def handle_crawl_data(data_list, dbpos, q):
    crawl_list = []
    pos = dbpos
    for each in data_list:
        if each['_pos'] > dbpos:
            crawl_list.append(each)
            q.put({'link': each['link'], '_id': each['_id']})
        else:
            return crawl_list, pos
        pos = data_list[-1]['_pos']
    return crawl_list, pos


def gather_content(q):
    print('处理正文的进程启动了，正在等待url...')
    dicts = []
    while True:
        try:
            url_dict = q.get(timeout=5)
            # print('拿到正文url', url_dict)
            dicts.append(url_dict)
            if len(dicts) >= 100:
                p0 = Process(target=handle_zhengwen(dicts))
                p0.start()
                p0.join()
                dicts = []
                time.sleep(random.randint(5, 10))
        except queue.Empty:
            if len(dicts) > 0:
                p0 = Process(target=handle_zhengwen(dicts))
                p0.start()
                p0.join()
            break


if __name__ == '__main__':
    u = UCstore()
    q = Queue()
    p = Process(target=gather_content, args=(q,))
    p.start()
    c = crawl_run(u.last_pos(), q)
    u.insert_list(c)
