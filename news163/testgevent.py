# -*- coding: utf-8 -*-
# 2017/2/8

import requests
from multiprocessing import Process
import time
import gevent
from gevent import monkey

monkey.patch_all()


def fetch(url):
    try:
        s = requests.Session()
        r = s.get(url, timeout=1)  # 在这里抓取页面
    except Exception as e:
        print(e)
    else:
        print(r.text)


def process_start(tasks):
    gevent.joinall(tasks)  # 使用协程来执行


def task_start(urllist):
    task_list = []
    # for url in urllist:
    #     task_list.append(gevent.spawn(fetch, url))
    gevent.joinall([
        gevent.spawn(fetch, 'http://temp.163.com/special/00804KVA/cm_shehui_02.js'),
        gevent.spawn(fetch, 'http://temp.163.com/special/00804KVA/cm_shehui_03.js'),
        gevent.spawn(fetch, 'http://temp.163.com/special/00804KVA/cm_shehui_04.js'),
        gevent.spawn(fetch, 'http://temp.163.com/special/00804KVA/cm_shehui_05.js'),
        gevent.spawn(fetch, 'http://temp.163.com/special/00804KVA/cm_shehui_06.js'),
        gevent.spawn(fetch, 'http://temp.163.com/special/00804KVA/cm_shehui_07.js'),
        gevent.spawn(fetch, 'http://temp.163.com/special/00804KVA/cm_shehui_08.js')
    ])


    # with open(filepath, 'r') as reader:
    #     url = reader.readline().strip()
    #     print(url)
    #     task_list = []
    #     i = 0
    #     while url != "":
    #         i += 1
    #         task_list.append(gevent.spawn(fetch, url))
    #         if i == flag:
    #             p = Process(target=process_start, args=(task_list,))
    #             p.start()
    #             task_list = []
    #             i = 0
    #
    #     if len(task_list) > 0:
    #         p = Process(target=process_start, args=(task_list,))
    #         p.start()


if __name__ == '__main__':
    ulist = [
        "http://temp.163.com/special/00804KVA/cm_shehui_02.js",
        "http://temp.163.com/special/00804KVA/cm_shehui_03.js",
        "http://temp.163.com/special/00804KVA/cm_shehui_04.js",
        "http://temp.163.com/special/00804KVA/cm_shehui_05.js",
        "http://temp.163.com/special/00804KVA/cm_shehui_06.js",
        "http://temp.163.com/special/00804KVA/cm_shehui_07.js",
        "http://temp.163.com/special/00804KVA/cm_shehui_08.js"
    ]

    start = time.time()
    task_start(ulist)
    print('{0:.6f}'.format(time.time() - start))
