# -*- coding: utf-8 -*-
# 2016/11/8
# author = JEFF

import requests

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
}

proxies = {
    'http': '124.88.67.24:843'
}

response = requests.get('http://music.163.com', headers=headers, proxies=proxies)
print(response.status_code)
print(response.headers)