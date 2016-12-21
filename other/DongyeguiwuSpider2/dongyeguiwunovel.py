# -*- coding: utf-8 -*-
# 2016/12/14

'''
http://www.dongyeguiwu.com/

spider novel

'''

import random
import requests
import re
import os
import time
import lxml.html
import redis
from multiprocessing.dummy import Pool as Pool
from other.DongyeguiwuSpider.novel import Novel
from other.DongyeguiwuSpider.novel import Chapter


class DownNovel(object):
    def __init__(self):
        self.base_url = 'http://www.dongyeguiwu.com/'
        self.red = redis.Redis()
        self.spider_list = 'nov'
        desktop = os.path.join(os.path.expanduser("~"), 'Desktop')
        self.base_dir = os.path.join(desktop, 'dongyeguiwu')
        self.base_error_logging = os.path.join(self.base_dir, 'error.txt')
        self.re_find_fenye = re.compile('<div id="fenye" class="fenye">(.*?)</div>', re.S)
        # self.re_parse_fenye = re.compile('</span>(.*?)下一页', re.S)
        # self.re_parse_nextpage = re.compile('<a href="(.*?)">下一页</a>', re.S)
        self.re_parse_page_span = re.compile('<span>(.*?)</span>', re.S)
        if not os.path.exists(self.base_dir):
            os.mkdir(self.base_dir)

    # 请求页面
    def get_page(self, url):
        time.sleep(random.randint(3, 5))
        try:
            response = requests.get(url)
            if response.status_code is not 200:
                print(url, 'spider defeated')
                print(url, 'spider defeated')
                print(url, 'spider defeated')
            return response.content.decode()
        except Exception as e:
            print(e)
            with open(self.base_error_logging, 'a') as f:
                f.write('spider page:{} defeated'.format(url) + ' ' + time.strftime("%Y-%m-%d %H:%M:%S") + '\n')
            time.sleep(20)
            self.get_page(url)

    # 收集需要下载书的URL
    # def parse_home_page(self):
    #     home_html = self.get_page(self.base_url)
    #     selector = lxml.html.fromstring(home_html)
    #     title = selector.xpath('//div[@class="booktable"]')
    #     ul = title[0].xpath('ul')
    #     li_list = ul[1].xpath('li')
    #     for n, i in enumerate(li_list):
    #         book_url = i.xpath('a/@href')[0]
    #         book_name = i.xpath('a/text()')[0]
    #         self.red.rpush(self.spider_list, book_url)

    # 拿到所有要下载的书的URL
    def get_book_list(self):
        book_old_list = self.red.lrange(self.spider_list, 0, -1)
        book_new_list = []
        for book in book_old_list:
            book_new_list.append(book.decode())
        return book_new_list

    # 解析每个书的URL，准备下载
    def parse_book(self, url):
        html = self.get_page(url)
        selector = lxml.html.fromstring(html)
        # 获取书名
        book_name = selector.xpath('//div[@id="top"]')[0].xpath('span/a/text()')[2]
        booktable = selector.xpath('//div[@class="booktable"]')[0]
        book_ul = booktable.xpath('ul')[1]
        # 章节URL集合
        chapter_url_list = book_ul.xpath('li/a/@href')
        # 章节名集合
        chapter_name_list = book_ul.xpath('li/a/text()')
        # 创建对象
        novel = Novel()
        novel.name = book_name
        novel.chapter_name_list = chapter_name_list
        novel.chapter_url_list = chapter_url_list
        self.down_book(novel)

    # 下载每本书
    def down_book(self, novel):
        if novel is None:
            return None
        # 创建文件夹
        book_dir = os.path.join(self.base_dir, novel.name)
        if not os.path.exists(book_dir):
            os.mkdir(book_dir)
        book_path = os.path.join(book_dir, '{}.txt'.format(novel.name))
        with open(book_path, 'a', encoding='utf-8') as f:
            f.write('    {}  东野圭吾'.format(novel.name))
        for n, i in enumerate(novel.chapter_url_list):
            # if n > 1:
            #     break
            self.down_detail_page(i, book_path, novel.name)

    # 下载每一章节
    def down_detail_page(self, url, book_path, novel_name):
        # 解析每个章节
        html = self.get_page(url)
        print('down', url)
        # 创建一个章节对象
        chapter = Chapter()
        selector = lxml.html.fromstring(html)
        chapter_name = selector.xpath('//div[@class="pt"]//a/text()')
        # 章节名
        chapter.chapter = chapter_name[0]
        # 章节内容
        content_list = selector.xpath('//div[@class="readtext"]/p/text()')
        chapter.content = '\n\n'.join(content_list)

        # 判断是否有分页
        fenye_re = re.search(self.re_find_fenye, html)
        if fenye_re:
            str = fenye_re.group(1)
            page_span = re.findall(self.re_parse_page_span, str)
            # if page_span:
            count = max(page_span)
            new_list = ['{0}/{1}'.format(url, c) for c in range(int(count) + 1) if c >= 2]
            for new in new_list:
                fenye_html = self.get_page(new)
                fenye_selector = lxml.html.fromstring(fenye_html)
                fenye_content_list = fenye_selector.xpath('//div[@class="readtext"]/p/text()')
                fenye_content = '\n\n'.join(fenye_content_list)
                chapter.content = chapter.content + '\n\n' + fenye_content
        with open(book_path, 'a', encoding='utf-8') as f:
            f.write('\n\n\n\n')
            f.write('    {}'.format(chapter.chapter))
            f.write('\n\n\n\n')
            f.write('    {}'.format(chapter.content))
            f.write('\n')
        print('                          {}{} is success...'.format(novel_name, chapter_name))

    def do_main(self):
        book_list = self.get_book_list()
        pool = Pool(4)
        pool.map(self.parse_book, book_list)


if __name__ == '__main__':
    down_novel = DownNovel()
    start_time = time.time()
    down_novel.do_main()
    print('spider consumes for {} seconds'.format(time.time() - start_time))
