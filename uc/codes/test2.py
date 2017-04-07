# -*- coding: utf-8 -*-
# 2017/3/31

import time
import datetime


def timestamp2date(timestamp):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(str(timestamp)[:-3])))


def strdate2timestamp(strdate):
    timeStamp = int(time.mktime(time.strptime(strdate, '%Y-%m-%dT%H:%M:%S.000+0800')))
    return timeStamp * 1000


if __name__ == '__main__':
    at = [1, 2, 123, 3251, 23211, 32]
    print(at[2])
    print(at[5])
    print(at[-1])
    print(at[-2])
    # print(timestamp2date(1488627172101))
