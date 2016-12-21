# -*- coding: utf-8 -*-
# 2016/12/21
# author = JEFF
import http
import random
import re

import requests

url = 'http://www.dongyeguiwu.com/'
test_url = 'http://www.baidu.com'


# response = requests.get(url)
# html = response.content.decode()
#
# print(html)

class Proxy(object):
    def __init__(self, protocol, ip, port):
        self.protocol = protocol
        self.ip = ip
        self.port = port

    def assemble(self):
        return '{}://{}:{}'.format(self.protocol, self.ip, self.port)


proxies = []

pro_urls = ['http://www.mimiip.com/gngao/{}'.format(i) for i in range(1, 6)]

html = requests.get(pro_urls[0]).content.decode()
# print(html)
rows = re.findall(r'<tr>[\s\S]*?</tr>', html)
for row in rows:
    try:
        ip = re.search(r'\d+\.\d+\.\d+\.\d+', row).group(0)
        port = re.search(r'<td>(\d{2,4})</td>', row).group(1)
        protocol = re.search(r'<td>(HTTP|HTTPS)</td>', row).group(1).lower()
        proxies.append(Proxy(protocol, ip, port))
    except IndexError:
        pass
    except AttributeError:
        pass

proxies_list = []

for pro in proxies:
    proxies_list.append(pro.assemble())


def _judge(proxy):
    """
    decide whether this proxy is alive

    :param proxy:
    :return:
    """
    print(proxy)
    split = str(proxy).split('://')
    proxies = {
        split[0]: proxy
    }

    try:
        requests.get(test_url, proxies=proxies)
    except(IOError, http.client.HTTPException):
        print('d')
        print('d')
        print('d')
        return False
    print('t')
    print('t')
    print('t')
    return True


proxy = random.choice(proxies_list)
print(proxy)
_judge(proxy)
