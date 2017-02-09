# -*- coding: utf-8 -*-
# 2017/2/9

import logging
import time


def log_current_date():
    return time.strftime('%Y%m%d')


class Logger(object):
    def __init__(self, logname='{}.log'.format(log_current_date()), log='163news'):
        self.logger = logging.getLogger(log)
        self.logger.setLevel(logging.DEBUG)

        fh = logging.FileHandler(logname)
        fh.setLevel(logging.ERROR)

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # formatter = format_dict[int(loglevel)]
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def get_logger(self):
        return self.logger


if __name__ == '__main__':
    logger = Logger().get_logger()
    logger.info('xxxx info')
    logger.error('xxx error')
