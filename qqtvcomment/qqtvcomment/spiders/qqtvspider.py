# -*- coding: utf-8 -*-
# 2016/10/24
# author = JEFF

import scrapy
import re
import json
from qqtvcomment.items import QqtvcommentItem
from qqtvcomment.utils import getstrtime


class QqtvSpider(scrapy.Spider):
    name = "qqtvcommentspider"
    start_url = "http://v.qq.com/x/cover/qviv9yyjn83eyfu.html?vid=l00173o64p7"
    ncgi_url = "http://ncgi.video.qq.com/fcgi-bin/video_comment_id?otype=json&op=3&vid=%s"
    comm_url = "http://coral.qq.com/article/%s/comment?commentid=0&reqnum=10"
    hot_comm_url = "http://coral.qq.com/article/%s/hotcomment?reqnum=10"
    vid = start_url.split('?vid=')[1]

    def start_requests(self):
        urls = [
            'http://v.qq.com/x/cover/qviv9yyjn83eyfu.html?vid=l00173o64p7'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        c_url = self.ncgi_url % self.vid
        yield scrapy.Request(url=c_url, callback=self.parse_id)

    def parse_id(self, response):
        vid = re.search('"comment_id":"(.*?)"', response.body.decode('utf-8'), re.S).group(1)
        # 获取最新评论
        # get_comm_url = self.comm_url % vid
        # print(get_comm_url)
        # 获取热评
        get_comm_url = self.hot_comm_url % vid
        yield scrapy.Request(url=get_comm_url, callback=self.parse_comment)

    def parse_comment(self, response):
        cont = response.body.decode('utf-8')
        jsDict = json.loads(cont)
        jsData = jsDict['data']
        comment = jsData['commentid']
        for comm in comment:
            item = QqtvcommentItem()
            content = comm['content']
            if content == "" or len(content) == 0:
                continue
            item['content'] = content
            item['name'] = comm['userinfo']['nick']
            time = getstrtime(comm['time'])
            item['ctime'] = time
            yield item
