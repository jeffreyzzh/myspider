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
        book_dir = book_path(bookinfo.text)
        print(bookinfo.get('href'))
        print(bookinfo.text)
        handlebook(bookinfo.get('href'), book_dir)


def handlebook(bookurl, book_dir):
    book_page = downpage(bookurl)
    selector = etree.HTML(book_page)
    chapters = selector.xpath('//div[@class="booktable"]//li[@class="chapters"]/a')
    for each in chapters:
        print(each.get('href'))
        print(each.text)
        handlechapter(each.get('href'), book_dir, each.text)


def full_url(rurl, page):
    return rurl + '/' + str(page)


def handlechapter(chapterurl, book_dir, chaptername):
    chapter_page = downpage(chapterurl)
    selector = etree.HTML(chapter_page)
    content = list()
    # 先判断有没分页
    have_fenye = selector.xpath('//div[@class="fenye"]')
    if have_fenye:
        # 有分页
        ps = selector.xpath('//div[@class="text"]//p')
        for each in ps:
            # print(each.text)
            content.append(each.text)
        fenyes = have_fenye[0].xpath('./a')
        for page in range(2, len(fenyes)):
            fenye_html = downpage(full_url(chapterurl, page))
            xpaths = etree.HTML(fenye_html)
            ps = xpaths.xpath('//div[@class="text"]//p')
            for each in ps:
                # print(each.text)
                content.append(each.text)
    else:
        # 无分页,直接处理
        ps = selector.xpath('//div[@class="text"]//p')
        for each in ps:
            # print(each.text)
            content.append(each.text)
    chapter_path = os.path.join(book_dir, '{}.txt'.format(chaptername))
    with open(chapter_path, 'w', encoding='utf-8') as f:
        for each in content:
            f.write(each)
            f.write('\r\n')


if __name__ == '__main__':
    # indexpage()

    # url1 = 'http://www.dongyeguiwu.com/books/baiyexing'
    # url2 = 'http://www.dongyeguiwu.com/books/x'
    # handlebook(url2)

    # chapter_url = 'http://www.dongyeguiwu.com/books/baiyexing/53.html'
    # handlechapter(chapter_url, None, None)

    init_dir()
    indexpage()
    pass
