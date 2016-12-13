# -*- coding: utf-8 -*-
# 2016/12/11 0011
# JEFF

spider_course_url = [
    # 'https://www.shiyanlou.com/courses/359',
    # 'https://www.shiyanlou.com/courses/30',
    # 'https://www.shiyanlou.com/courses/31',
    # 'https://www.shiyanlou.com/courses/70',
    # 'https://www.shiyanlou.com/courses/49',
    # 'https://www.shiyanlou.com/courses/427',
    # 'https://www.shiyanlou.com/courses/354',
    'https://www.shiyanlou.com/courses/348',
    'https://www.shiyanlou.com/courses/388',
    'https://www.shiyanlou.com/courses/387'
]


def get_spider_list():
    return spider_course_url


def get_spider_url():
    return spider_course_url.pop()
