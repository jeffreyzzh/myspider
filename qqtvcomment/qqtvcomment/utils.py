# -*- coding: utf-8 -*-
# 2016/10/24 0024
# author = JEFF

import time


def getstrtime(seconds):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(seconds))

if __name__ == '__main__':
    time = getstrtime(1477313345)
    print(time)

