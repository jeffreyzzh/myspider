# -*- coding: utf-8 -*-

import scrapy


class QqtvcommentItem(scrapy.Item):
    name = scrapy.Field()
    content = scrapy.Field()
    ctime = scrapy.Field()
