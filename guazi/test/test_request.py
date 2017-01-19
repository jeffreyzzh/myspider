# -*- coding: utf-8 -*-
# 2017/1/19

import requests
from bs4 import BeautifulSoup as bs

resp = requests.get(url='https://www.baidu.com', proxies={'http': 'http://121.232.146.106:9000'})
resp.encoding = 'utf-8'
soup = bs(resp.text, 'lxml')
print(soup.title)
print(dir(resp))
print(resp.headers)
