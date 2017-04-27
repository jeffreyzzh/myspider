# -*- coding: utf-8 -*-
# 2017/4/26

import re
import time
import redis
import chardet
import requests
from lxml import etree
from urllib.parse import urljoin
from weather_spider.spider_weather_store import Store
from weather_spider.spider_weather_dao import Weather
from weather_spider.settings import *


def clean_str(s):
    return s.strip().replace(' ', '').replace('\r', '').replace('\n', '')


def is_prase(url):
    is_p = re.search('http://www.tianqihoubao.com/guoji/\d{1,4}/\d{4}-\d{1,2}.html', url)
    if is_p:
        return True
    return False


def fetch(url):
    print('we get >> {}'.format(url))
    try:
        resp = requests.get(url, timeout=(3.05, 27))
        if resp.status_code != 200:
            return fetch(url)
        char = chardet.detect(resp.content)
        try:
            return resp.content.decode(char['encoding'])
        except Exception:
            resp.encoding = 'gbk'
            return resp.content.decode('gbk')
    except Exception as e:
        print(e)
        return fetch(url)


def parse_html_link(html):
    selector = etree.HTML(html)
    links = selector.xpath('//a/@href')
    for link in links:
        u = urljoin(START_URL, link)
        if 'guoji' not in u:
            continue
        r.rpush(do_crawl, u)


def parse_html_weather(html):
    title = re.search('<title>(.*?)</title>', html, re.S).group(1)
    print(title)
    city = re.findall(u'(.*?)历史', title.strip())[0]
    selector = etree.HTML(html)
    weathers = selector.xpath('//*[@id="content"]/table/tr')
    for index in range(1, len(weathers)):
        w = weathers[index]
        w_temp = w.xpath('./td[3]')[0].text
        temps = clean_str(w_temp).split('/')
        wea = Weather(
            scw_city=city,
            scw_time=clean_str(w.xpath('./td[1]')[0].text).replace('年', '-').replace('月', '-').replace('日', ''),
            scw_weather=clean_str(w.xpath('./td[2]')[0].text),
            scw_temp_h=temps[0],
            scw_temp_l=temps[1],
            scw_wind=clean_str(w.xpath('./td[4]')[0].text),
            scw_create_time=time.strftime("%Y-%m-%d %H:%M:%S"),
            scw_crawl_time=time.strftime("%Y-%m-%d 00:00:00"),
            scw_ispull=0,
            scw_pull_time='0000-00-00 00:00:00'
        )
        store.insert(wea)


def main():
    while r.lrange(do_crawl, 0, 1):
        url = r.lpop(do_crawl)
        if r.sismember(crawld, url):
            continue
        html = fetch(url.decode())
        parse_html_link(html)
        if is_prase(url.decode()):
            parse_html_weather(html)
        r.sadd(crawld, url)


if __name__ == '__main__':
    START_URL = 'http://www.tianqihoubao.com/guoji/'
    # db
    store = Store()
    # redis
    pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT)
    r = redis.Redis(connection_pool=pool)
    do_crawl = 'scb_weather_to_crawl'
    crawld = 'scb_weather_crawld'
    # start
    r.rpush(do_crawl, START_URL)
    main()
