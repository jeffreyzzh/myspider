# -*- coding: utf-8 -*-
# 17/1/18

import asyncio
import requests
import time
from bs4 import BeautifulSoup as bs


async def do_requests(url):
    print('wget url:{}'.format(url))
    html = await get_request(url)
    return html


async def get_request(url):
    resp = requests.get(url)
    return resp.text


async def do_main(url):
    html = await do_requests(url)
    print('url {} title is :{}'.format(url, parse_page(html)))


def parse_page(html):
    soup = bs(html, 'lxml')
    return soup.title


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    tasks = [
        do_main('http://www.baidu.com'),
        do_main('http://www.163.com'),
        do_main('http://www.sina.com.cn'),
        do_main('http://www.qq.com'),
        do_main('http://www.jd.com'),
        do_main('http://www.weibo.com'),
        do_main('http://www.youku.com')
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
