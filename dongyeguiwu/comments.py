# -*- coding: utf-8 -*-
# 17/3/21

import requests
import traceback


def downpage(url, trycount=1):
    if not url:
        return None
    try:
        resp = requests.get(url, timeout=3)
        return resp.text
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        return downpage(url, trycount=trycount + 1)


if __name__ == '__main__':
    url = 'http://www.dongyeguiwu.com/books'
    html = downpage(url)
    print(html)
