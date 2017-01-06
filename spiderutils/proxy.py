# -*- coding: utf-8 -*-
# 2016/12/29

import re
import socket
import random
import http.client
import requests
from abc import ABCMeta, abstractmethod
from urllib.error import HTTPError, URLError


class Proxy(object):
    def __init__(self, protocol, ip, port):
        self.protocol = protocol
        self.ip = ip
        self.port = port

    def assemble(self):
        return '{}://{}:{}'.format(self.protocol, self.ip, self.port)


class IProxyFinder(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def find(self):
        """returns a list of Proxy objects"""
        pass


class MimiProxyFinder(IProxyFinder):
    def __init__(self):
        """http://www.mimiip.com/gngao/"""
        self.urls = ['http://www.mimiip.com/gngao/{}'.format(i + 1) for i in range(5)]

    def find(self, *args):
        proxies = []
        try:
            # response = requests.get(random.choice(self.urls))
            response = requests.get(self.urls[0])
        except Exception:
            return proxies
        html = response.text
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

        return proxies


def judge_proxy(proxy, test_url='http://www.baidu.com'):
    pro_name = proxy.assemble()
    proxys = {
        proxy.protocol: pro_name
    }
    try:
        response = requests.get(test_url, proxies=proxys, timeout=3)
        if response.status_code != 200:
            print('proxy judge excetion: code != 200')
            return False
    except requests.exceptions.RequestException:
        print('proxy judge excetion')
        return False
    print('{} is alive'.format(pro_name))
    return True
