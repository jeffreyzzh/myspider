# -*- coding: utf-8 -*-
# 17/3/21

import requests
import os
import traceback

desktop = os.path.join(os.path.expanduser("~"), 'Desktop')
base_dir = os.path.join(desktop, 'dongyeguiwu')


def downpage(url, trycount=1):
    if not url:
        return None
    try:
        resp = requests.get(url, timeout=3)
        return resp.text
    except Exception as e:
        # print(e)
        # print(traceback.format_exc())
        return downpage(url, trycount=trycount + 1)


def init_dir():
    if not os.path.exists(base_dir):
        os.mkdir(base_dir)


def book_path(bookname):
    _book_path = os.path.join(base_dir, bookname)
    if not os.path.exists(_book_path):
        os.mkdir(_book_path)
    return _book_path


if __name__ == '__main__':
    # url = 'http://www.dongyeguiwu.com/books'
    # html = downpage(url)
    # print(html)
    p = book_path('白夜行')
    print(p)
