# -*- coding: utf-8 -*-
# 2017/2/13 0013
# JEFF

import requests

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': '_zap=ae58bb63-f28e-4e85-8c80-969c89352458; d_c0="AFCAVU0XmwqPTrABzq5iK705V4SxBJF8MBw=|1474986674"; _za=51774a99-1e3f-4fe0-b85e-0e80fdfd731c; _zap=a0bd9e53-37c1-4462-92d9-5ec5a1458394; q_c1=3e837d95bd7a4bb7b21082ce601acd43|1484389182000|1474986719000; _xsrf=e4983ec83d41e53e2d657bbc6c8e4f90; aliyungf_tc=AQAAAMx42WU6UgsAYvKC28s8TdsHwj7J; l_cap_id="MDU4YmM2YWNhMTAxNDliNDljYmJiNWRlODFhNzI3N2I=|1486991482|05861255e8689ed40316c67e84cbf5dfb936efc3"; cap_id="Y2JhNGUyOTg2NWEyNDAxM2E1NmQ1NzA0MDA3ZjFiNGI=|1486991482|b8ed5bf5542fb3861d538db814c2e892f08405ef"; login="NGNmY2QxNDY1Yzg0NGY1NDlkNzM0ZGZhNGZmNzIxYjQ=|1486991495|1541923238736d6b8cbff74b1cc770d1a4a35a96"; n_c=1; __utma=51854390.1440648995.1486211341.1486984542.1486990874.3; __utmb=51854390.0.10.1486990874; __utmc=51854390; __utmz=51854390.1486990874.3.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=51854390.100-1|2=registration_date=20150324=1^3=entry_date=20150324=1; z_c0=Mi4wQUtBQVl5d20wd2NBVUlCVlRSZWJDaGNBQUFCaEFsVk5qejNKV0FCbHdlRnlnWWp1MmdsM0gtSEFTdWZuaTBfV2lR|1486993292|f16fea3ed5e2c8f7e68ded83a8c1fe8d546e6557',
    'Host': 'www.zhihu.com',
    'Referer': 'https://www.zhihu.com/question/55313155/answer/145491147',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36',
}

resp = requests.get('https://www.zhihu.com/question/55313155', headers=headers)
print(resp.text)
