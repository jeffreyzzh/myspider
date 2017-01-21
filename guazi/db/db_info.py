# -*- coding: utf-8 -*-
# 2017/1/21

import sys
import time
from guazi.db.common_getset_info import GetAndSet

gs = GetAndSet()


def dayurls():
    while True:
        carurl_coll = gs.get_mongo_dayurls()
        counts = carurl_coll.find().count()
        sys.stdout.write(counts + '\r\n')
        sys.stdout.flush()
        time.sleep(5)
