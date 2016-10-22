# -*- coding: utf-8 -*-
# 2016/10/21 0021
# author = JEFF

import scrapy
import re
from bs4 import BeautifulSoup
from novel.items import NovelItem


class NovelSpider(scrapy.Spider):
    name = "novel"

    def start_requests(self):
        urls = [
            'http://www.daomubiji.com'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        selector = scrapy.Selector(response)
        tables = selector.xpath('//table')
        for table in tables:
            book_name = table.xpath('tr/td/center/h2/text()').extract()[0]
            print(book_name)
            title = table.xpath('tr/td/a/text()').extract()
            print(title)
            url = table.xpath('tr/td/a/@href').extract()
            print(url)
            for i in range(len(url)):
                item = NovelItem()
                item['book_name'] = book_name
                item['chapter_url'] = url[i]
                book_list = title[i].split(' ')
                try:
                    item['book_title'] = book_list[0]
                    item['chapter_num'] = book_list[1]
                    item['chapter_name'] = book_list[2]
                except Exception:
                    continue
                # yield item
                yield scrapy.Request(url=url[i], callback=self.parseContent, meta={'item': item})
                break

    def parseContent(self, response):
        selector = scrapy.Selector(response)
        item = response.meta['item']
        html = selector.xpath('//div[@class="content"]').extract()[0]
        print(html)
        re.search('<div class="content">')