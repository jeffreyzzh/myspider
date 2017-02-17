# -*- coding: utf-8 -*-
# 2017/2/17

import traceback

try:
    a = 10
    b = 0

    c = a / b
    print(c)
except Exception as e:
    print(e)
    print(traceback.format_exc())
