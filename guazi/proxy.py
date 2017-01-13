# -*- coding: utf-8 -*-
# 2017/1/6
# author = JEFF
import random
from bs4 import BeautifulSoup
from abc import ABCMeta, abstractmethod
import requests
import re

proxy_list = [
    'http://113.18.193.20:8080',
    'https://27.159.124.121:8118',
    'http://122.72.32.75:80',
    'https://222.243.176.51:8998',
    'http://113.18.193.4:8080',
    'http://124.88.67.32:81',
    'http://218.191.247.51:80',
    'http://113.18.193.21:8080',
    'https://58.49.222.210:8998',
    'https://112.26.103.94:8118',
    'http://124.88.67.34:81',
    'https://220.166.241.13:8118',
    'https://211.147.240.86:808',
    'http://124.88.67.52:843',
    'http://122.72.32.72:80',
    'https://49.85.16.3:8998',
    'http://222.33.192.238:8118',
    'https://117.79.93.39:8808',
    'http://117.21.234.96:8080',
    'https://113.26.90.15:8998',
    'https://125.31.19.27:80',
    'https://182.37.79.242:8118',
    'https://116.19.176.156:8118',
    'http://120.52.73.97:8081',
    'https://49.4.178.24:9000',
    'https://119.1.78.168:80',
    'https://121.57.139.36:8998',
    'https://117.57.212.93:8998',
    'http://211.75.115.20:80',
    'https://125.117.48.8:8998',
    'https://115.231.219.202:3128',
    'http://223.18.181.240:80',
    'http://120.52.21.132:8082',
    'http://124.88.67.18:843',
    'https://113.242.212.175:8998',
    'http://124.88.67.39:843',
    'https://222.87.124.138:8998',
    'https://106.91.29.229:8998',
    'https://27.19.111.187:8998',
    'https://58.208.27.181:8118',
    'https://115.237.19.232:8998',
    'https://119.254.92.53:80',
    'https://117.166.178.46:8118',
    'https://121.237.32.14:8998',
    'https://36.48.185.217:8998',
    'http://122.72.32.88:80',
    'https://111.61.35.76:8118',
    'http://124.88.67.17:843',
    'https://114.38.241.17:8998',
    'https://106.89.85.14:8998',
    'https://125.117.95.38:8998',
    'https://116.255.192.209:808'
]


def get_randon_proxy():
    proxy = random.choice(proxy_list)
    str = proxy.split(':')
    dict = {}
    dict[str[0]] = proxy
    return dict


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

