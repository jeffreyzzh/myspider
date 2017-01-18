# -*- coding: utf-8 -*-
# 2017/1/17

import re
from guazi.parse_request import requesturl


class PageParse(object):
    def parse_cat_url(self, url):
        html = requesturl(url)
