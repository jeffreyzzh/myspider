# -*- coding: utf-8 -*-
# 2016/10/20 0020
# author = JEFF

import scrapy
from douban.items import DoubanItem


class TutorialSpider(scrapy.Spider):
    name = "douban"
    url = "http://movie.douban.com/top250"

    def start_requests(self):
        urls = [
            'http://movie.douban.com/top250'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item = DoubanItem()
        selector = scrapy.Selector(response)
        movie = selector.xpath('//div[@class="info"]')
        for mov in movie:
            # 电影标题
            title = mov.xpath('div[@class="hd"]/a/span/text()').extract()
            full_title = ''
            for t in title:
                full_title = full_title + t
            # print(full_title)

            # 电影信息
            movie_info = mov.xpath('div[@class="bd"]/p/text()').extract()
            for info in movie_info:
                print(info)

            # 电影评分
            star = mov.xpath('div[@class="bd"]//span[@class="rating_num"]/text()').extract()[0]
            # print(star)

            # 电影短语
            quote = mov.xpath('div[@class="bd"]//span[@class="inq"]/text()').extract()
            if quote:
                quote = quote[0]
                # print(quote)
            else:
                quote = '这电影不错'

            item['title'] = full_title
            item['movie_info'] = ';'.join(movie_info)
            item['star'] = star
            item['quote'] = quote
            yield item

        # 爬取下一页
        next_url = selector.xpath('//span[@class="next"]/link/@href').extract()
        if next_url:
            print(next_url[0])
            yield scrapy.Request(url=self.url + next_url[0], callback=self.parse)


