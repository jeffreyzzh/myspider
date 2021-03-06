# -*- coding: utf-8 -*-
# 2016/12/22

import time


def current_time_full():
    return time.strftime('%Y-%m-%d %H:%M:%S')


def format_time_full(timex=None):
    if not timex:
        return current_time_full()
    else:
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timex))


def current_time_simple():
    return time.strftime('%Y-%m-%d')


if __name__ == '__main__':
    print(format_time_full(1485144582))
    print(format_time_full())
