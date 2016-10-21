# -*- coding: utf-8 -*-
# 2016/10/20 0020
# author = JEFF

import scrapy
from tutorial.items import TutorialItem


class TutorialSpider(scrapy.Spider):
    # name = "tutorial"
    # start_urls = ["https://movie.douban.com/top250"]
    #
    # def parse(self, response):
    #     print(response.body)

    # def parse(self, response):
    #     for sel in response.xpath('//ul/li'):
    #         item = TutorialItem()
    #         item['title'] = sel.xpath('a/text()').extract()
    #         item['link'] = sel.xpath('a/@href').extract()
    #         item['desc'] = sel.xpath('text()').extract()
    #         yield item

    name = "quotes"

    # def start_requests(self):
    #     urls = [
    #         'http://quotes.toscrape.com/page/1/',
    #         'http://quotes.toscrape.com/page/2/',
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)
    #
    # def parse(self, response):
    #     page = response.url.split("/")[-2]
    #     filename = 'quotes-%s.html' % page
    #     with open(filename, 'wb') as f:
    #         f.write(response.body)
    #     self.log('Saved file %s' % filename)

    def start_requests(self):
        urls = [
            'http://movie.douban.com/top250'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # page = response.url.split("/")[-2]
        # filename = 'top250.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)
        print(response.body)
        print(response.url)

