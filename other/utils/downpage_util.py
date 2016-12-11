# -*- coding: utf-8 -*-
# 2016/12/11 0011
# JEFF

def format_print(str):
    size = len(str)
    for each in range(size + 4):
        print('- ', end='')
    print()
    print('  {}'.format(str))
    for each in range(size + 4):
        print('- ', end='')
    print()
    print()


def get_header():
    return {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Host": "www.shiyanlou.com",
        "Accept-Encoding": "gzip, deflate, sdch",
        "Connection": "keep-alive",
        "Referer": "https://www.shiyanlou.com/courses/?course_type=all&tag=Python&fee=all",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36"
    }


format_print("你好")
