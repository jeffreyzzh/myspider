# -*- coding: utf-8 -*-
# 2016/10/24
# author = JEFF

import scrapy
import re
import json
from qqtvcomment.items import QqtvcommentItem


class QqtvSpider(scrapy.Spider):
    name = "qqtvcommentspider"
    ncgi_url = "http://ncgi.video.qq.com/fcgi-bin/video_comment_id?otype=json&op=3&vid=%s"
    comm_url = "http://coral.qq.com/article/%s/comment?commentid=0&reqnum=10"

    def start_requests(self):
        urls = [
            'http://v.qq.com/x/cover/qviv9yyjn83eyfu.html?vid=l00173o64p7'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        pass
