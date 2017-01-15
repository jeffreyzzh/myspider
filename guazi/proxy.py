# -*- coding: utf-8 -*-
# 2017/1/6
# author = JEFF
import random
from bs4 import BeautifulSoup
from abc import ABCMeta, abstractmethod
import requests
import re


class Proxy(object):
    def __init__(self, protocol, ip, port):
        self.protocol = protocol
        self.ip = ip
        self.port = port

    def assemble(self):
        return '{}://{}:{}'.format(self.protocol, self.ip, self.port)

    def getprotocol(self):
        return self.protocol

    def get_proxy_dict(self):
        return {
            self.getprotocol(): self.assemble()
        }


class IProxyFinder(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def find(self):
        """returns a list of Proxy objects"""
        pass


class MimiProxyFinder(IProxyFinder):
    def __init__(self):
        self.urls = ['http://www.mimiip.com/gngao/{}'.format(i + 1) for i in range(5)]

    def find(self):
        proxies = []
        for url in self.urls:
            resp = requests.get(url)
            html = resp.text
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


class KuaiProxyFinder(IProxyFinder):
    def __init__(self):
        self.urls = ['http://www.kuaidaili.com/proxylist/{}'.format(i + 1) for i in range(10)]

    def find(self):
        proxies = []
        for url in self.urls:
            resp = requests.get(url)
            html = resp.text
            rows = re.findall(r'<tr>(.*?)</tr>', html, re.S)
            for row in rows:
                try:
                    ip = re.search('<td data-title="IP">(.*?)</td>', row, re.S).group(1)
                    port = re.search('<td data-title="PORT">(.*?)</td>', row).group(1)
                    protocol = re.search(r'<td data-title="类型">(.*?)</td>', row).group(1).lower()
                    if ',' in protocol:
                        protocol = 'https'
                    proxies.append(Proxy(protocol, ip, port))
                except IndexError:
                    pass
                except AttributeError:
                    pass

        return proxies


class XiciProxyFinder(IProxyFinder):
    def __init__(self):
        self.urls = ['http://www.xicidaili.com/nn/{}'.format(i + 1) for i in range(5)]

    def find(self):
        proxies = []
        for url in self.urls:
            resp = requests.get(
                url, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36'
                }
            )
            soup = BeautifulSoup(resp.content.decode(), 'lxml')
            rows = soup.select('tr.odd')
            for row in rows:
                try:
                    alltd = row.select('td')
                    ip = alltd[1].text
                    port = alltd[2].text
                    protocol = alltd[5].text.lower()
                    proxies.append(Proxy(protocol, ip, port))
                except IndexError:
                    pass
                except AttributeError:
                    pass

        return proxies


class ProxyPool(object):
    def __init__(self, finder=MimiProxyFinder(), test_utl='http://www.baidu.com'):
        self.pool = set()
        self.test_url = test_utl
        self.finder = finder
        self.refresh()

    def refresh(self):
        self.pool = set(filter(self.__judge, set(self.finder.find())))

    def __judge(self, proxy):
        """decide whether this proxy is alive"""
        try:
            resp = requests.get(self.test_url, proxies=proxy.get_proxy_dict(), timeout=1)
            if resp.status_code != 200:
                return False
        except requests.exceptions.ConnectTimeout:
            return False
        except requests.exceptions.ProxyError:
            return False
        except requests.exceptions.ReadTimeout:
            return False
        except Exception as e:
            print(e)
            return False
        print('{} is ok'.format(proxy.assemble()))
        return True

    def get_proxy(self):
        return random.choice(list(self.pool))


if __name__ == '__main__':
    pool = ProxyPool(test_utl='https://www.guazi.com/gz/dazhong')
    while True:
        if input('next?') == 'no':
            break
        proxy = pool.get_proxy()
        print(proxy.get_proxy_dict())
        print(type(proxy.get_proxy_dict()))
