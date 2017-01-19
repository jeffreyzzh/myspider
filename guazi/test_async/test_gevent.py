# -*- coding: utf-8 -*-
# 2017/1/19

import gevent
import requests
from gevent import monkey

monkey.patch_all()


def f(url):
    print('GET: {}'.format(url))
    resp = requests.get(url)
    data = resp.text
    print('%d bytes received from %s.' % (len(data), url))


if __name__ == '__main__':
    gevent.joinall([
        gevent.spawn(f, 'http://www.baidu.com'),
        gevent.spawn(f, 'http://www.163.com'),
        gevent.spawn(f, 'http://www.sina.com.cn'),
        gevent.spawn(f, 'http://www.qq.com'),
        gevent.spawn(f, 'http://www.jd.com'),
        gevent.spawn(f, 'http://www.weibo.com'),
        gevent.spawn(f, 'http://www.youku.com')
    ])
