# -*- coding: utf-8 -*-
# 2017/2/7

import time

t = time.time()
print(str(t).replace(".", '')[:-4])


def current_time_full():
    return time.strftime('%Y-%m-%d %H:%M:%S')


def format_time_full(timex=None):
    if not timex:
        return current_time_full()
    else:
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timex))


a = format_time_full(1486443602825)
print(a)
