# -*- coding: utf-8 -*-
# 2017/1/17
# author = JEFF

import time


def current_time():
    return time.strftime('%Y-%m-%d %H:%M:%S')


def current_date():
    return time.strftime('%Y-%m-%d')


def log_current_date():
    return time.strftime('%Y%m%d')


if __name__ == '__main__':
    print(current_date())
    print(current_time())
    print(log_current_date())
