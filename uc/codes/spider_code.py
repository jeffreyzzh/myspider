# -*- coding: utf-8 -*-
# 2017/3/31

import asyncio
import re
import time

import aiohttp
import js2xml
import requests

from spiderutils.copyheaders2dict import get_headers
from uc.codes.UcStore import UCstore
from uc.codes.spider_logger import getlogger

logger = getlogger()
list_headers = get_headers('headers.txt')
zw_headers = get_headers('headers2.txt')

ajax_url = 'http://napi.uc.cn/3/classes/news_comments/categories/neirong/lists/617?_app_id=03b70b8484ae418789ebfec8ffa64820&_fetch=1&_max_age=1&_fetch_incrs=1&_size=200'
page_url = 'http://napi.uc.cn/3/classes/news_comments/categories/neirong/lists/617?_app_id=03b70b8484ae418789ebfec8ffa64820&_fetch=1&_max_age=1&_fetch_incrs=1&_size=200&_max_pos={}'

news_xpath = '//var[@name="xissJsonData"]'
title_xpath = './/property[@name="title"]/string'
content_xpath = './/property[@name="content"]/string'
source_xpath = './/property[@name="source_name"]/string'
origin_xpath = './/property[@name="origin_src_name"]/string'
publish_xpath = './/property[@name="publish_time"]/number'


def fet_url(pos=''):
    return page_url.format(pos)


def fetch(url, headers, data):
    error_count = 0
    try:
        resp = requests.get(url, headers=headers, data=data, timeout=3)
        if resp.status_code != 200:
            print(url, 'status_code', resp.status_code)
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


def fetch_zhengwen(url):
    return fetch(url, headers=zw_headers, data=None)


async def async_fetch(d, error_count=0):
    if error_count >= 5:
        logger.error('{} to much error'.format(d['link']))
        return ''
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(d['link']) as response:
                html = await response.text()
                return html + ',.|' + d['_id']
    except Exception as e:
        logger.error(e)
        return await async_fetch(d, error_count=error_count + 1)


async def handle_async_fetch(dicts):
    store = UCstore()
    start = time.time()
    count = 1
    tasks = [async_fetch(d) for d in dicts]
    pages = await asyncio.gather(*tasks)
    for page in pages:
        html, id = page.split(',.|')
        jsoncont = re.search('(try {.*?)</script>', html, re.S)
        if not jsoncont:
            continue
        try:
            selector = js2xml.parse(jsoncont.group(1)).xpath(news_xpath)[0]
            content_dict = {
                '_id': id,
                '_title': selector.find(title_xpath).text,
                '_content': re.subn('</?\w+>|<!--.*?-->', '', selector.find(content_xpath).text)[0],
                '_source': selector.find(source_xpath).text,
                '_origin': selector.find(origin_xpath).text,
                '_publish': selector.find(publish_xpath).get('value')
            }
            print(count)
            print(content_dict)
            store.update_content(content_dict)
        except Exception as e:
            print(e)
            logger.error(e)
            logger.error(html)
            logger.error(jsoncont)
        count += 1
    end = time.time()
    print(end - start)


def handle_zhengwen(dicts):
    # for each in dicts:
    #     html = fetch_zhengwen(each['link'])
    #     jsoncont = re.search('(try {.*?)</script>', html, re.S)
    #     if not jsoncont:
    #         return
    #     selector = js2xml.parse(jsoncont.group(1)).xpath(news_xpath)[0]
    #     print({
    #         '_id': each['_id'],
    #         '_title': selector.find(title_xpath).text,
    #         '_content': re.subn('</?\w+>|<!--.*-->', '', selector.find(content_xpath).text)[0],
    #         '_source': selector.find(source_xpath).text,
    #         '_origin': selector.find(origin_xpath).text,
    #         '_publish': selector.find(publish_xpath).get('value')
    #     })
    #     break
    loop = asyncio.get_event_loop()
    loop.run_until_complete(handle_async_fetch(dicts))
    # loop.close()


def do_test(url):
    html = fetch_zhengwen(url)
    jsoncont = re.search('(try {.*?)</script>', html, re.S)
    if not jsoncont:
        return
    cont = jsoncont.group(1).strip()
    parsed = js2xml.parse(cont)
    print(js2xml.pretty_print(parsed))
    # title = parsed.xpath('//property[@name="title"]/string')[0]
    new = parsed.xpath(news_xpath)[0]
    title = new.find(title_xpath)
    print(new.find(content_xpath).text)
    content, size = re.subn('</?\w+>|<!--.*-->', '', new.find(content_xpath).text)
    source = new.find(source_xpath)
    origin = new.find(origin_xpath)
    publish = new.find(publish_xpath)
    print(title.text)
    print(content)
    print(source.text)
    print(origin.text)
    print(publish.get('value'))
    print()
    print()


if __name__ == '__main__':
    do_test(
        'http://m.uczzd.cn/webapp/webview/article/news.html?aid=16749977856522694278&cid=100&zzd_from=uc-iflow&uc_param_str=dndseiwifrvesvntgi&recoid=$')
