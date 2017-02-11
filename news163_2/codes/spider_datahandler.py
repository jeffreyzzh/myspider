# -*- coding: utf-8 -*-
# 2017/2/11 0011
# JEFF

from news163_2.codes.spider_base import BaseClass


class Darahandler(object):
    def __init__(self):
        self.logger = BaseClass.getlogger()

    def handler_ajax_new(self, new):
        if not new or not isinstance(new, dict):
            print('false')
        print(new)


def gethandler():
    return Darahandler()


if __name__ == '__main__':
    dh = Darahandler()
    dh.handler_ajax_new(
        {
            'name': 'jeffrey',
            'age': 25
        }
    )
