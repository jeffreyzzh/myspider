# -*- coding: utf-8 -*-
# 2017/1/21
import queue

from guazi2.parse.parse4url import GuaziParse
import time
from multiprocessing import Pool
from guazi2.db.common_getset_info import GetAndSet
from guazi2.init_do.common_pageurl import PageUrl

gs = GetAndSet()
pu = PageUrl()
area1, area2, cars, cartypes = gs.get_all_info()


def coll_all_links():
    for car in cars:
        url = pu.get_path(car=car)
        yield url


def coll_all_links2():
    for a in gs.get_gd_area():
        if a != '_id':
            for car in cars:
                url = pu.get_path(area=a, car=car)
                yield url


def do_parse(url):
    # gp = GuaziParse(url)
    # gp.carpage()
    print(url)
    # print(' * - ' * 20)
    # print('url', gp.get_all_links())
    # print()


def dotest(*urls):
    gp = GuaziParse()
    for i in urls:
        print(i)
        gp.put_url(i)
    gp.carpage()


if __name__ == '__main__':
    start = time.time()

    gp = GuaziParse(isproxy=False)
    links = [u for u in coll_all_links2()]
    for each in links:
        gp.put_url(each)

    gp.carpage()

    # coll_all_links2()

    print(time.time() - start)
