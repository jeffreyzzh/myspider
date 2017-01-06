# -*- coding: utf-8 -*-
# 2017/1/6

import requests

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    'Cookie': '_T_WM=ee400d2ae9059c337dee4a842d814b13; SUB=_2A251a2ECDeRxGeBO7FsW9SjJzj-IHXVWlA9KrDV6PUJbkdBeLWatkW1RfbTMMJvteaHBkuH6bJyWz2lFCg..; SUHB=0d4-V_WR_YSqrZ; SCF=AkGcdWJykTjOABFcz-6xWj1aQaDCK6A5gn6_Pnenoos1m58vXjft3X0aJ4L4m_u-b5Bu680TNrwEMWzS2p_ofDQ.; SSOLoginState=1483673938; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D1076031644948230%26fid%3D2302831644948230%26uicode%3D10000011',
    'Host': 'm.weibo.cn',
    'Referer': 'http://m.weibo.cn/?jumpfrom=weibocom',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
    'X-Requested-With': 'XMLHttpRequest'
}

resp = requests.get('http://m.weibo.cn/feed/friends?version=v4&next_cursor=4060871610782375&page=1', headers=headers)
print(resp.content.decode())
