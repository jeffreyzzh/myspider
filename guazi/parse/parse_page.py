# -*- coding: utf-8 -*-
# 2017/1/17


import time
from urllib.parse import urljoin

import lxml.html

from guazi.parse.parse_request import requesturl
from guazi.settings import RequestSETTING
from guazi2.tool.log import Logger


class CarUrlParse(object):
    def __init__(self, base_url):
        self.logger = Logger(RequestSETTING.pageurl_logfile_name(), RequestSETTING.pageurl_log_name()).get_logger()
        self.url_list = []
        self.base_url = base_url
        self.verify_key = base_url.split('.com')[1][0:3]

    def get_linkscount(self):
        return len(self.url_list)

    def get_urls(self):
        return self.url_list

    def do_main(self, url=None, page=1):
        if not url:
            url = self.base_url
        self.logger.info('spider page:{}, url:{}'.format(page, url))
        next_page = self.parse_car_url(url)
        self.logger.info('links now have: {}'.format(self.get_linkscount()))
        if next_page:
            self.logger.info('准备翻页')
            time.sleep(2)
            self.do_main(next_page, page=page + 1)
        else:
            print('crawl end.')

    def parse_car_url(self, url):
        if not url:
            return None
        html = requesturl(url)
        selector = lxml.html.fromstring(html)
        cars = selector.xpath(
            '//p[@class="infoBox"]/a[@baidu_alog="pc_list_xiangqingye&click&pc_list_xiangqingye_c"]/@href'
        )
        for car in cars:
            if not car.startswith(self.verify_key):
                continue
            full_url = urljoin(url, car)
            self.url_list.append(full_url)
        cut_off = selector.xpath('//div[@class="cut-off-txt"]')
        if cut_off:
            return None
        next_page = self.carpage_isnext(selector)
        if next_page:
            return next_page
            # return None
        else:
            return None

    def carpage_isnext(self, selector):
        next_page = selector.xpath('//a[@class="next"]')
        if next_page:
            return urljoin(self.base_url, next_page[0].get('href'))
        else:
            return None


if __name__ == '__main__':
    start = time.time()
    url = 'https://www.guazi.com/gz/hafei'
    page = CarUrlParse(url)
    page.do_main()
    print(page.get_linkscount())
    print(time.time() - start)
