# -*- coding: utf-8 -*-
# 2017/1/17

import lxml.html
from urllib.parse import urljoin

import time

from guazi.parse_request import requesturl


class PageParse(object):
    def __init__(self):
        pass

    def parse_car_url(self, url):
        html = requesturl(url)
        selector = lxml.html.fromstring(html)
        cars = selector.xpath('//a[@baidu_alog="pc_list_xiangqingye&click&pc_list_xiangqingye_c"]')
        for car in cars:
            href = car.get('href')
            yield urljoin(url, href)
        next_page = self.carpage_isnext(selector)
        if next_page:
            time.sleep(1)
            print(1)
            self.parse_car_url(next_page)


    def carpage_isnext(self, selector):
        next_page = selector.xpath('//a[@class="next"]')
        if next_page:
            return urljoin(url, next_page[0].get('href'))


if __name__ == '__main__':
    url = 'https://www.guazi.com/gz/toyota/'
    page = PageParse()
    urls = [u for u in page.parse_car_url(url)]
    for each in urls:
        print(each)
    print(len(urls))
