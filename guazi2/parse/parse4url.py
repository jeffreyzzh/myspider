# -*- coding: utf-8 -*-
# 2017/1/21
import random
import time
from guazi2.db.common_getset_info import GetAndSet
from guazi2.parse.parse_requests import GuaziRequest
from guazi2.tool.log import logger
from urllib.parse import urljoin
import lxml.html
import queue


class GuaziParse(object):
    def __init__(self, isproxy=True):
        self.isproxy = isproxy
        self.logger = logger
        self.request = GuaziRequest(isproxy=self.isproxy)
        self.queue = queue.Queue()
        self.parse_list = []
        self.xpath_expression = '//p[@class="infoBox"]/a[@baidu_alog="pc_list_xiangqingye&click&pc_list_xiangqingye_c"]/@href'
        gs = GetAndSet()
        self.url_coll = gs.get_mongo_dayurls()

    def put_url(self, url):
        self.queue.put(url)

    def get_url(self):
        return self.queue.get(timeout=3)

    def carpage(self):
        while True:
            try:
                time.sleep(random.randint(15, 30))
                url = self.queue.get(True, timeout=10)
                print('----' * 6, url)
                html = self.request.do_requests(url)
                has_next = self.parse_carpage(html, url)
                if has_next:
                    self.queue.put(has_next)
            except queue.Empty:
                break
            except Exception as e:
                self.logger.error(e)

    def parse_carpage(self, html, url):
        if not html:
            print('no html!!!!!!!!!!!!!!')
            print('no html!!!!!!!!!!!!!!')
            print('no html!!!!!!!!!!!!!!')
            print('no html!!!!!!!!!!!!!!')
            print('no html!!!!!!!!!!!!!!')
            self.logger.error('{} no html'.format(url))
            return None
        # print(html)
        verify_key = url.split('.com')[1][0:3]
        selector = lxml.html.fromstring(html)
        cars = selector.xpath(self.xpath_expression)
        for car in cars:
            if not car.startswith(verify_key):
                continue
            full_url = urljoin(url, car)
            self.url_coll.insert({'url': full_url})
            print(full_url)

            # self.parse_list.append(urljoin(url, car))
        if selector.xpath('//div[@class="cut-off-txt"]'):
            return None
        next_page = self.carpage_isnext(selector, url)
        if next_page:
            return next_page
        else:
            return None

    def carpage_isnext(self, selector, url):
        next_page = selector.xpath('//a[@class="next"]')
        if next_page:
            return urljoin(url, next_page[0].get('href'))
        else:
            return None

    def get_all_links(self):
        return self.parse_list


if __name__ == '__main__':
    gp = GuaziParse()
    # gp.carpage()
    gp.put_url('https://www.guazi.com/gz/honda/')
    gp.put_url('https://www.guazi.com/gz/audi/')
    gp.carpage()
