# -*- coding: utf-8 -*-
# 2017/1/13

# 测试
import random

import requests

url = 'https://www.guazi.com/gz/dazhong'

plist = [
    # {'https': 'https://106.91.35.241:8998'},
    # {'https': 'https://183.66.81.178:8998'}
    {'http': 'http://203.70.11.186'}
]

resp = requests.get(url, proxies=random.choice(plist), timeout=5)
print(resp.status_code)
print(resp.content.decode())
