# -*- coding: utf-8 -*-
# 2016/12/11 0011
# JEFF

spider_course_url = [
    'https://www.shiyanlou.com/courses/708'
]


def get_spider_list():
    return spider_course_url


def get_spider_url():
    return spider_course_url.pop()
