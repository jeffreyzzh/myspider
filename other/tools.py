# -*- coding: utf-8 -*-
# 2016/12/22

import time


def current_time_full():
    return time.strftime('%Y-%m-%d %H:%M:%S')


def current_time_simple():
    return time.strftime('%Y-%m-%d')


if __name__ == '__main__':
    print(current_time_simple())
