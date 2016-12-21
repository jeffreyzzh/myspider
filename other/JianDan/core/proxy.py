# -*- coding: utf-8 -*-
# 2016/12/15

import re
import socket
import random
import http.client
from abc import ABCMeta, abstractmethod
from urllib.error import URLError, HTTPError

from core.fetch import build_fetch


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
        """
        returns a list of Proxy objects

        :return:
        """
        pass


class MimiProxyFinder(IProxyFinder):
    def __init__(self):
        self.urls = ['http://www.mimiip.com/gngao/{}'.format(i) for i in range(5)]

    def find(self, fenth=None):
        if not fenth:
            fetch = build_fetch()
        proxies = []
        try:
            html = fetch(random.choice(self.urls))
        except IOError:
            return proxies
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


class ProxyPool:
    def __init__(self, finder, test_url='http://www.baidu.com'):
        self.source_page = 'http://www.mimiip.com/gngao/'
        self.pool = set()
        self.test_url = test_url
        self.finder = MimiProxyFinder()

    def refresh(self):
        self.pool = set(filter(lambda p: self._judge(p), self.pool))
        if len(self.pool) < 10:
            if len(self.pool) > 0:
                fetch = build_fetch(proxy=list(self.pool)[0])
            else:
                fetch = None
            new_proxies = filter(lambda p: self._judge(p), self.finder.find(fetch))
            for new_proxy in new_proxies:
                self.pool.add(new_proxy)

    def random_proxy(self):
        return random.choice(list(self.pool))

    def _judge(self, proxy):
        """
        decide whether this proxy is alive

        :param proxy:
        :return:
        """
        fetch = build_fetch(proxy=proxy, timeout=1)
        try:
            fetch(self.test_url)
        except(IOError, http.client.HTTPException):
            return False

        return True
