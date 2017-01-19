# -*- coding: utf-8 -*-
# 2017/1/19
import random

import requests
import json

touse_list = []
unuse_list = []


def get_ips():
    r = requests.get('http://127.0.0.1:8000/?types=0&count=10&country=国内')
    ip_ports = json.loads(r.text)

    for ip in ip_ports:
        ip_dict = {
            'http': 'http://{}:{}'.format(ip[0], ip[1]),
            'https': 'https://{}:{}'.format(ip[0], ip[1])
        }
        touse_list.append(ip_dict)


def get_one_ip():
    return random.choice(touse_list)


def mark_unuse_ip(ip_dict):
    if ip_dict in touse_list:
        touse_list.remove(ip_dict)
        unuse_list.append(ip_dict)


if __name__ == '__main__':
    get_ips()
    info = get_one_ip()

    url = 'http://icanhazip.com/'
    r1 = requests.get(url)
    r1.encoding = 'utf-8'
    print(r1.text)

    try:
        r2 = requests.get(url, proxies=info)
        r2.encoding = 'utf-8'
        print(r2.text)
    except Exception as e:
        print(e)
        r3 = requests.get(url, proxies=get_one_ip())
        r3.encoding = 'utf-8'
        print(r3.text)
