# -*- coding: utf-8 -*-
# 2017/1/17
# author = JEFF

from guazi.tool.time_tool import *


class RequestSETTING(object):
    REQUEST_LOGFILE_NAME = '{}request'.format(log_current_date())
    REQUEST_LOG_NAME = 'request-log'

    @staticmethod
    def request_logfile_name():
        return RequestSETTING.REQUEST_LOGFILE_NAME

    @staticmethod
    def request_log_name():
        return RequestSETTING.REQUEST_LOG_NAME


if __name__ == '__main__':
    print(RequestSETTING.request_logfile_name())
    print(RequestSETTING.request_log_name())
