# -*- coding: utf-8 -*-
# 17/3/21

from lxml import etree
from dongyeguiwu.comments import *

index_url = 'http://www.dongyeguiwu.com/books'


def indexpage():
    index_page = downpage(index_url)
    selector = etree.HTML(index_page)
    books = selector.xpath('//div[@class="booktable"]//li[starts-with(@class, "cat-item")]')
    if not books:
        print('do not hava content, program end.')
        exit()
    for each in books:
        bookinfo = each.xpath('./a')[0]
        print(bookinfo.get('href'))
        print(bookinfo.text)


def handlebook(bookurl):
    book_page = downpage(bookurl)
    selector = etree.HTML(book_page)
    chapters = selector.xpath('//div[@class="booktable"]//li[@class="chapters"]/a')
    for each in chapters:
        print(each.get('href'))
        print(each.text)


def handlechapter(chapterurl):
    chapter_page = downpage(chapterurl)
    selector = etree.HTML(chapter_page)
    # 先判断有没分页
    have_fenye = selector.xpath('//div[@class="fenye"]')
    if have_fenye:
        # 有分页
        fenyes = have_fenye[0].xpath('./a')
        for page in range(2, len(fenyes)):
            print(page)
        ps = selector.xpath('//div[@class="text"]//p')
        for each in ps:
            print(each.text)
    else:
        # 无分页,直接处理
        ps = selector.xpath('//div[@class="text"]//p')
        for each in ps:
            print(each.text)


def handlepagedetail(page_url):
    page_detail = downpage(page_url)


if __name__ == '__main__':
    # indexpage()

    # url1 = 'http://www.dongyeguiwu.com/books/baiyexing'
    # url2 = 'http://www.dongyeguiwu.com/books/x'
    # handlebook(url2)

    chapter_url = 'http://www.dongyeguiwu.com/books/baiyexing/53.html'
    handlechapter(chapter_url)
    pass
