# -*- coding: utf-8 -*-
# 2017/1/19
import gevent
from gevent import monkey
from gevent import pool
import requests
import time
from bs4 import BeautifulSoup as bs

gevent.monkey.patch_all()


def do_requests(url):
    print('wget url:{}'.format(url))
    html = requests.get(url).text
    return html


def do_main(url):
    html = do_requests(url)
    print('url {} title is :{}'.format(url, parse_page(html)))


def parse_page(html):
    soup = bs(html, 'lxml')
    return soup.title


if __name__ == '__main__':
    # start = time.time()
    # do_main('http://www.baidu.com'),
    # do_main('http://www.163.com'),
    # do_main('http://www.sina.com.cn'),
    # do_main('http://www.qq.com'),
    # do_main('http://www.jd.com'),
    # do_main('http://www.weibo.com'),
    # do_main('http://www.youku.com')
    # end = time.time()
    # print(end - start)

    start = time.time()
    gevent.joinall([
        gevent.spawn(do_main, 'http://www.baidu.com'),
        gevent.spawn(do_main, 'http://www.163.com'),
        gevent.spawn(do_main, 'http://www.sina.com.cn'),
        gevent.spawn(do_main, 'http://www.qq.com'),
        gevent.spawn(do_main, 'http://www.jd.com'),
        gevent.spawn(do_main, 'http://www.weibo.com'),
        gevent.spawn(do_main, 'http://www.youku.com')
    ])
    # ulist = [
    #     'http://www.baidu.com',
    #     'http://www.163.com',
    #     'http://www.sina.com.cn',
    #     'http://www.qq.com',
    #     'http://www.jd.com',
    #     'http://www.weibo.com',
    #     'http://www.youku.com'
    # ]
    # for u in ulist:
    #     do_main(u)
    end = time.time()
    print(end - start)
