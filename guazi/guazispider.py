# -*- coding: utf-8 -*-
# 2017/1/19

from guazi.parse.parse_page import CarUrlParse
from guazi.db.common_getset_info import GetAndSet
from guazi.init_do.common_parse import ParsePage
from guazi.init_do.common_pageurl import PageUrl
from guazi.parse.parse_page import CarUrlParse

# p = CarUrlParse('https://www.guazi.com/gz/dazhong/')
# p.do_main()
# print(p.get_linkscount())


if __name__ == '__main__':
    gs = GetAndSet()
    url_obj = PageUrl()
    area1, area2, cars, cartypes = gs.get_all_info()
    for car in cars:
        url = url_obj.get_path(car=car)
        page_obj = CarUrlParse(url)
        page_obj.do_main()
        all_urls = page_obj.get_urls()
        for each in all_urls:
            print(each)
            # print(url)
