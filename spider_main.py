#!F:\myproject\xxx\Scripts\python.exe
# -*- coding: utf-8 -*-
# 2017/2/15

import time

from news163_2.news163spider import News163Spider

if __name__ == '__main__':
    start = time.time()

    n = News163Spider()
    n.domain()

    print('{0:.6f}'.format(time.time() - start))
