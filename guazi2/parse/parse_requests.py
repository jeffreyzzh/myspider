# -*- coding: utf-8 -*-
# 2017/1/21
import random
import requests
import json
import re
from guazi2.tool.ua import get_ua_dict
from guazi2.tool.log import logger
from guazi2.tool.time_tool import log_current_date


class GuaziRequest(object):
    def __init__(self, isproxy=True):
        self.logger = logger
        self.re_code = re.compile('<input class="code-input" placeholder="请输入验证码" name="verification_code">', re.S)
        self.down_img = re.compile('<img class="code-img" src="(.*?)"></img>', re.S)
        self.proxy_list = []
        self.get_proxies()
        self.isproxy = isproxy

    def get_one_proxy(self):
        if len(self.proxy_list) <= 1:
            self.refresh_proxypool()
        return random.choice(self.proxy_list)

    def get_proxies(self):
        r = requests.get('http://127.0.0.1:8000/?types=0&count=60')
        ip_ports = json.loads(r.text)
        for uip in ip_ports:
            ip_dict = {
                'http': 'http://{}:{}'.format(uip[0], uip[1]),
                'https': 'https://{}:{}'.format(uip[0], uip[1])
            }
            self.proxy_list.append(ip_dict)

    def refresh_proxypool(self):
        self.proxy_list.clear()
        r = requests.get('http://127.0.0.1:8000/?types=0&count=60')
        ip_ports = json.loads(r.text)
        for uip in ip_ports:
            ip_dict = {
                'http': 'http://{}:{}'.format(uip[0], uip[1]),
                'https': 'https://{}:{}'.format(uip[0], uip[1])
            }
            self.proxy_list.append(ip_dict)

    def del_one_proxy(self, proxies):
        unuse_ip = proxies['http'].replace('http://', '').split(':')[0]
        self.proxy_list.remove(proxies)
        requests.get('http://127.0.0.1:8000/delete?ip={}'.format(unuse_ip))
        if len(self.proxy_list) <= 10:
            self.refresh_proxypool()

    def do_requests(self, url, count=1):
        if count >= 5:
            self.logger.error('{} to much error...'.format(url))
            return None
        try:
            if self.isproxy:
                proxies = self.get_one_proxy()
                print(proxies)
            else:
                proxies = None
            resp = requests.get(url, proxies=proxies, headers=get_ua_dict(), timeout=5)
            if resp.status_code != 200:
                return self.do_requests(url, count=count)
            resp.encoding = 'utf-8'
            html = resp.text
            if self.has_verification_code(html):
                print('yan -- zheng -- ma !!')
                print('yan -- zheng -- ma !!')
                print('yan -- zheng -- ma !!')
                print('yan -- zheng -- ma !!')
                print('yan -- zheng -- ma !!')
                print('yan -- zheng -- ma !!')
                print('yan -- zheng -- ma !!')
                print('yan -- zheng -- ma !!')
                self.del_one_proxy(proxies)
                return self.do_requests(url, count=count)
            return html
        except Exception as e:
            self.logger.error(e)
            return self.do_requests(url, count=count + 1)

    def has_verification_code(self, html):
        if re.search(self.re_code, html):
            img = re.search(self.down_img, html)
            if img:
                code_url = img.group(1)
                with open('verification_code.png', 'wb') as f:
                    f.write(requests.get(code_url).content)
            return True
        return False


if __name__ == '__main__':
    gr = GuaziRequest()
    html = gr.do_requests('https://www.guazi.com/gz/honda/')
    print(html)
