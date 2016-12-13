# -*- coding: utf-8 -*-
# 2016/12/13

# 收集所要爬取的URL

import re
import requests
import redis
import time
import lxml.html
import urllib.parse


class CollectURL(object):
    def __init__(self):
        self.start_url = 'https://www.shiyanlou.com/courses/?course_type=all&tag=Java&fee=all'
        self.r = redis.Redis()
        self.spider_queue = 'shiyanlou_spider'
        self.re_r1 = re.compile('<a aria-label="Next" href="(.*?)">', re.S)

    def do_main(self):
        # response = requests.get(self.start_url)
        # # 200
        # if response.status_code is not 200:
        #     pass
        # print(response.content.decode())
        # html = response.content.decode()
        # with open(r"C:\Users\Administrator\Desktop\a.html", 'w', encoding='utf-8') as f:
        #     f.write(html)
        self.parse_page(self.start_url)

    def down_page(self, url):
        return requests.get(url).content.decode()

    def parse_page(self, url):
        html = self.down_page(url)
        selector = lxml.html.fromstring(html)
        course_list = selector.xpath('//div[@class="col-md-4 col-sm-6  course"]')
        for each in course_list:
            money = each.xpath('a/div/span[@class="course-money pull-right"]')
            if len(money) is not 0:
                continue
            href = each.xpath('a/@href')[0]
            course_url = urllib.parse.urljoin(self.start_url, href)
            print(course_url)
            self.r.sadd(self.spider_queue, course_url)
        next_a = re.search(self.re_r1, html)
        if next_a:
            print(next_a.group(1))
            url = next_a.group(1)
            full_url = urllib.parse.urljoin(self.start_url, url)
            print(full_url)
            self.parse_page(full_url)

    def do_main2(self):
        with open(r"C:\Users\Administrator\Desktop\a.html", 'r', encoding='utf-8') as f:
            html = f.read()

        selector = lxml.html.fromstring(html)
        course_list = selector.xpath('//div[@class="col-md-4 col-sm-6  course"]')
        for each in course_list:
            money = each.xpath('a/div/span[@class="course-money pull-right"]')
            if len(money) is not 0:
                continue
            href = each.xpath('a/@href')[0]
            course_url = urllib.parse.urljoin(self.start_url, href)
            print(course_url)
            self.r.sadd(self.spider_queue, course_url)


if __name__ == '__main__':
    c = CollectURL()
    start_time = time.time()
    c.do_main()
    print(time.time() - start_time)
