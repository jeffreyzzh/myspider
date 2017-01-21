# -*- coding: utf-8 -*-
# 2017/1/10

import logging
from guazi2.tool.time_tool import log_current_date


class Logger(object):
    def __init__(self, logname, log):
        self.logger = logging.getLogger(log)
        self.logger.setLevel(logging.DEBUG)

        fh = logging.FileHandler(logname)
        fh.setLevel(logging.DEBUG)

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
    logger = Logger('{}.log'.format(log_current_date()), 'splog').get_logger()
    logger.info('xxxx')
    logger.error('xxx')
