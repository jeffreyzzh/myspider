# -*- coding: utf-8 -*-
# 2017/2/11 0011
# JEFF

from news163_2.codes.spider_logger import getlogger


class BaseClass(object):
    def __init__(self):
        print("init!!!!!!!!!!!!!")

    logger = getlogger()

    @staticmethod
    def getlogger():
        return BaseClass.logger
