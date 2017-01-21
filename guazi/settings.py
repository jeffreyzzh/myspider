# -*- coding: utf-8 -*-
# 2017/1/17
# author = JEFF


class RequestSETTING(object):
    REQUEST_LOGFILE_NAME = '{}request.log'.format(log_current_date())
    REQUEST_LOG_NAME = 'request-log'

    PAGE_LOGFILE_NAME = '{}pageurl.log'.format(log_current_date())
    PAGE_LOG_NAME = 'page-log'

    REQUEST_TIMEOUT = 3
    REQUEST_COUNTS = 5

    @staticmethod
    def request_counts():
        return RequestSETTING.REQUEST_COUNTS

    @staticmethod
    def request_timeout():
        return RequestSETTING.REQUEST_TIMEOUT

    @staticmethod
    def request_logfile_name():
        return RequestSETTING.REQUEST_LOGFILE_NAME

    @staticmethod
    def request_log_name():
        return RequestSETTING.REQUEST_LOG_NAME

    @staticmethod
    def pageurl_logfile_name():
        return RequestSETTING.PAGE_LOGFILE_NAME

    @staticmethod
    def pageurl_log_name():
        return RequestSETTING.PAGE_LOG_NAME


class DBSETTING(object):
    DB_NAME = 'guazi'
    COLL_NAME = '{}urls'.format(log_current_date())

    @staticmethod
    def db_name():
        return DBSETTING.DB_NAME

    @staticmethod
    def coll_name():
        return DBSETTING.COLL_NAME


class EXCEPTIONINFO(object):
    FALSETOMUCH = 'Too many times of failure'
    REQUEST_EXCEPTION = 'request exception'

    @staticmethod
    def false_count_info():
        return EXCEPTIONINFO.FALSETOMUCH

    @staticmethod
    def request_false_info():
        return EXCEPTIONINFO.REQUEST_EXCEPTION


if __name__ == '__main__':
    print(RequestSETTING.request_logfile_name())
    print(RequestSETTING.request_log_name())

    print(DBSETTING.db_name())
    print(DBSETTING.coll_name())
